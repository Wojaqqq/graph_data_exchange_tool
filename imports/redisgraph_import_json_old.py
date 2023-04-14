import redis
import json
from redisgraph import Graph


def replace_chars(string):
    return string.replace("\'", "\\'")

# Connect to the Redis server
r = redis.Redis(host='172.18.0.5', port=6379)
graph_name = 'graph_from_json'

# Create a new graph in RedisGraph
redis_graph = Graph(graph_name, r)

with open('../out/neo4j_export.json') as file:
    for line in file.readlines():
        line_json = json.loads(line)
        type = line_json['type']

        if type == 'node':
            properties = ""
            for property in line_json['properties']:
                property_name = property.replace(" ", "_")
                if properties != "":
                    properties += ", "

                properties += f"{property_name}: "
                value = line_json['properties'][property]

                if isinstance(value, str):
                    value = replace_chars(value)
                    value = f"'{value}'"
                properties += str(value)
            query = f"MERGE (:{line_json['labels'][0]} {{id: {line_json['id']}, {properties}}})"
            print(query)
            # r.execute_command('GRAPH.QUERY', graph_name, query)
