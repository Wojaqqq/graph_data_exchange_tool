from py2neo import Graph
from pathlib import Path
from config import neo4j_config


def neo4j_export_csv(output: Path) -> None:
    graph = Graph(neo4j_config['host'], auth=(neo4j_config["user"], neo4j_config["password"]))
    query = """
        CALL apoc.export.csv.all(null, {
            stream: true
        })
        YIELD file, nodes, relationships, properties, data
        RETURN file, nodes, relationships, properties, data
    """

    result = graph.run(query)
    csv = result.data()[0]['data']

    with open(output / "neo4j_export.csv", 'w') as file:
        file.write(csv)
