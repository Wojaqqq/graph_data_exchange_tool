from py2neo import Graph
from config import neo4j_config
from pathlib import Path


def neo4j_export_cypher(output: Path) -> None:
    graph = Graph(neo4j_config['host'], auth=(neo4j_config["user"], neo4j_config["password"]))
    query = """
        CALL apoc.export.cypher.all(null, {
            format: 'updateAll',
            stream: true,
            useTypes: true
        })
        YIELD cypherStatements
        RETURN cypherStatements;
    """

    result = graph.run(query)
    cypher = result.data()[0]['cypherStatements']

    with open(output / 'neo4j_export.cypher', 'w') as file:
        file.write(cypher)
