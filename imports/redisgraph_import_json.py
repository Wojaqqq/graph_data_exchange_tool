import json
import redis
from redisgraph import Graph
from pathlib import Path


def redisgraph_import_json(output: Path) -> None:
    graph_name = 'movie_graph'

    r = redis.Redis(host='172.18.0.3', port=6379)
    redis_graph = Graph(graph_name, r)

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
        redis_graph.query(query)

    for edge in data['edges']:
        edge['start_id'] = id_dict[edge['start_id']]
        edge['end_id'] = id_dict[edge['end_id']]
        del edge['id']

        query = f"""
        MATCH (a), (b) WHERE a.id = {edge['start_id']} AND b.id = {edge['end_id']} CREATE (a)-[:{edge['label']}]->(b)
        """
        redis_graph.query(query)
