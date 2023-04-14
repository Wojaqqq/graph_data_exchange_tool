import argparse
from exports.neo4j_export_csv import neo4j_export_csv
from exports.age_export_json import age_export_json
from imports.age_import_csv import age_import_csv
from imports.redisgraph_import_csv import redisgraph_import_csv
from imports.neo4j_import_json import neo4j_import_json
from imports.redisgraph_import_json import redisgraph_import_json
from pathlib import Path
import warnings

warnings.filterwarnings("ignore")


def create_folder(user_input) -> Path:
    working_dir = Path.cwd() / user_input
    if not working_dir.is_dir():
        print(f"Creating folder {user_input}")
        working_dir.mkdir(parents=True, exist_ok=True)
    return working_dir


def parse_arguments():
    parser = argparse.ArgumentParser(description='Graph Converter')
    parser.add_argument('-s', '--src', dest='src', action='store',
                        help="from which database [neo4j, redis-graph, apache AGE]", required=True)
    parser.add_argument('-d', '--dest', dest='dest', action='store',
                        help="to which database [neo4j, redis-graph, apache AGE]", required=True)
    parser.add_argument('-w', '--workingdir', nargs='?', dest="working_dir", default='working_dir', type=create_folder,
                        help='directory with temporary files')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()

    if args.src.lower() == 'neo4j' and args.dest.lower() in ('apache', 'apache age', 'age'):
        neo4j_export_csv(args.working_dir)
        age_import_csv(args.working_dir)

    elif args.src.lower() == 'neo4j' and args.dest.lower() in ('redis-graph', 'redis'):
        neo4j_export_csv(args.working_dir)
        redisgraph_import_csv(args.working_dir)

    elif args.src.lower() in ('apache', 'apache age', 'age') and args.dest.lower() == 'neo4j':
        age_export_json(args.working_dir)
        neo4j_import_json(args.working_dir)

    elif args.src.lower() in ('apache', 'apache age', 'age') and args.dest.lower() in ('redis-graph', 'redis'):
        age_export_json(args.working_dir)
        redisgraph_import_json(args.working_dir)

    else:
        print("Cannot convert graph")
        exit(1)

    print("Conversion ended successfully")
