from pathlib import Path
from py2neo import Graph
from config import neo4j_config


def neo4j_export_cypher(output: Path) -> None:
    graph = Graph(neo4j_config['host'], auth=(neo4j_config["user"], neo4j_config["password"]))
    query = """
        CALL apoc.export.json.all(null, {
            writeNodeProperties: true,
            stream: true
        })
        YIELD data
        RETURN data;
    """

    result = graph.run(query)
    json = result.data()[0]['data']

    with open(output / 'neo4j_export.json', 'w') as file:
        file.write(json)
