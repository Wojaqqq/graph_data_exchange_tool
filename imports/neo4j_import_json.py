import json
from py2neo import Graph
from pathlib import Path


def neo4j_import_json(output: Path) -> None:
    graph = Graph("bolt://localhost:7687", auth=("neo4j", "neo4jpassword"))

    with open(output / 'age_export.json') as file:
        data = json.load(file)

    id_dict = {}

    for node in data['nodes']:
        params = ''
        for key, param in node["properties"].items():
            try:
                val = float(param)
            except:
                val = f'"{param}"'
            params = params + f' {key}: {val},'
            if key == "id":
                id_dict[node['id']] = param
        params = params[:-1]

        query = f'MERGE ({node["label"]}{{{params} }})'
        result = graph.run(query)

    for edge in data['edges']:
        edge['start_id'] = id_dict[edge['start_id']]
        edge['end_id'] = id_dict[edge['end_id']]
        del edge['id']

        query = f"""
        MATCH (a), (b) WHERE a.id = {edge['start_id']} AND b.id = {edge['end_id']} CREATE (a)-[:{edge['label']}]->(b)
        """
        result = graph.run(query)
