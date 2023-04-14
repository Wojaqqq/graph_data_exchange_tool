import psycopg2
from config import age_config
from pathlib import Path


def age_export_json(output: Path) -> None:
    conn = psycopg2.connect(host=age_config['host'], port=age_config["port"], dbname=age_config["dbname"],
                            user=age_config["user"], password=age_config["password"])

    graph_name = 'movie_graph'
    query = f"""
        LOAD 'age';
        SET search_path = ag_catalog, "$user", public;
    """

    with conn.cursor() as cursor:
        cursor.execute(query)

    query = f"""
    SELECT * 
        FROM cypher('{graph_name}', $$
            MATCH (n)
            RETURN n
    $$) as (e agtype);
    """
    with conn.cursor() as cursor:
        cursor.execute(query)
        nodes = cursor.fetchall()

    conn.commit()

    query = f"""
    SELECT * 
        FROM cypher('{graph_name}', $$
            MATCH () -[n]-()
            RETURN n
    $$) as (e agtype);
    """
    with conn.cursor() as cursor:
        cursor.execute(query)
        edges = cursor.fetchall()

    conn.commit()

    with open(output / 'age_export.json', 'w') as file:
        json = "{\"edges\": ["
        for edge in edges:
            json += f"{edge[0]},\n"
        json = json[:-2]

        json = json.replace("::\"edge\"", "")
        json = json.replace("::edge", "")

        json += "],\n"

        json += "\"nodes\": ["
        for node in nodes:
            json += f"{node[0]},\n"
        json = json[:-2]
        json += "]}"
        json = json.replace("::\"vertex\"", "")
        json = json.replace("::vertex", "")

        file.write(json)
