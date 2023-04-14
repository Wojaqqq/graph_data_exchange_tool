import pandas as pd
import psycopg2
from pathlib import Path
from config import age_config


def age_import_csv(output: Path) -> None:
    conn = psycopg2.connect(host=age_config['host'], port=age_config["port"], dbname=age_config["dbname"],
                            user=age_config["user"], password=age_config["password"])
    graph_name = 'movie_graph'
    query = f"""
        LOAD 'age';
        SET search_path = ag_catalog, "$user", public;
        SELECT create_graph('{graph_name}');
    """

    with conn.cursor() as cursor:
        cursor.execute(query)

    import_csv = pd.read_csv(output / 'neo4j_export.csv')

    break_column_name = '_start'
    nodes = pd.DataFrame()
    relations = pd.DataFrame()
    active_df = nodes

    for idx, col in enumerate(import_csv.columns):
        if col == break_column_name:
            active_df = relations
        active_df[col] = import_csv[col]

    nodes.dropna(how='all', subset=None, inplace=True)
    relations.dropna(how='all', subset=None, inplace=True)

    # relations.to_csv('../out/Relations.csv')

    node_values = nodes['_labels'].unique()
    rows_to_drop = [node_value for node_value in node_values if 'UNIQUE IMPORT LABEL' in node_value]
    for row_to_drop in rows_to_drop:
        nodes = nodes[nodes["_labels"].str.contains(row_to_drop) == False]

    node_values = nodes['_labels'].unique()
    for node_type in node_values:
        node_data = nodes[nodes['_labels'] == node_type]
        filename = f'../out/{node_type.replace(":", "")}.csv'
        node_data.dropna(how='all', axis=1, inplace=True)
        # node_data.to_csv(filename)

        for node in node_data.iloc:
            params = ''
            for param in node_data.columns:
                if not param.startswith('_'):
                    val = node[param]
                    if not pd.isna(val):
                        try:
                            val = float(val)
                        except:
                            val = f'"{val}"'
                        params = params + f', {param}: {val}'
            query = f'SELECT * FROM cypher(\'{graph_name}\', $$ CREATE ({node["_labels"]} {{id: {node["_id"]} {params} }}) $$) as (n agtype)'
            with conn.cursor() as cursor:
                cursor.execute(query)
    conn.commit()

    for node in relations.iloc:
        query = f"""
            SELECT * 
                FROM cypher('{graph_name}', $$
                    MATCH (a), (b) 
                    WHERE a.id = {node['_start']} AND b.id = {node['_end']} 
                    CREATE (a)-[:{node['_type']}]->(b)
                $$) as (e agtype);
        """
        with conn.cursor() as cursor:
            cursor.execute(query)
    conn.commit()
