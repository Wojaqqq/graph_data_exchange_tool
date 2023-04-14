# Wymiana danych grafowych

Celem projektu jest przegląd formatów i sposobów wymiany danych grafowych oraz ich zastosowanie w Neo4J, Apache AGE oraz redis-graph. Oczywistym formatem są zrzuty w języku [Cypher](https://en.wikipedia.org/wiki/Cypher_(query_language)), ale istnieje szereg innych formatów, które należy porównać pod względem siły ekspresji (szczególnie w zestawieniu z modelami danych poszczególnych narzędzi) i wsparcia w narzędziach.

# Autorzy

- [Tomasz Wojakowski](https://github.com/Wojaqqq)
- [Bartosz Nieroda](https://github.com/qymaensheel)
- [Krzysztof Pala](https://github.com/pallovsky)

# Dokumentacja

Narzędzie *graph_converter* pozwala na import oraz eksport grafów pomiędzy bazami danych: **Neo4j, Apache AGE, Redis-Graph**. W ramach projektu zostały zrealizowane następujące opcje transferu:

- Neo4j -> Redis-Graph
- Neo4j -> Apache AGE
- Apache AGE -> Neo4j
- Apache AGE -> Redis-Graph


## Instrukcja użycia

Konwersji można dokonać używając pythonowego skryptu *graph_converter.py*. Do skryptu muszą zostać przekazane następujące parametry:
- **--src** - źródłowa baza danych. Dostępne opcje: neo4j, age
- **--dest** - docelowa baza danych. Dostępne opcje: neo4j, redis-graph, age
- **--workingdir** - (opcjonalnie) ścieżka do folderu w którym będą generowane pliki pośrednie. Wartość domyślna: ./output
```
>> python graph_converter.py --help

usage: graph_converter.py [-h] -s SRC -d DEST [-w [WORKING_DIR]]

Graph Converter

options:
  -h, --help            show this help message and exit
  -s SRC, --src SRC     from which database [neo4j, redis-graph, apache AGE]
  -d DEST, --dest DEST  to which database [neo4j, redis-graph, apache AGE]
  -w [WORKING_DIR], --workingdir [WORKING_DIR]
                        directory with temporary files
```

## Konfiguracja

W celu zmiany ustawień dostępów do baz danych należy zmodyfikować plik *config.py*. Przykład:

```python
neo4j_config = {
    "host": "bolt://localhost:7687",
    "user": "neo4j",
    "password": "neo4jpassword"
}

redisgraph_config = {
    "host": "172.18.0.3",
    "port": 6379
}

age_config = {
    "host": "172.18.0.6",
    "port": "5432",
    "dbname": "apache-age",
    "user": "postgres",
    "password": "postgres"
}
```

## Użycie

Przed użyciem programu należy stworzyć wirtualne środowisko oraz zainstalować wymagania:
```bash
>> virtualenv venv
>> source venv/bin/activate
>> pip install -r requirements.txt
```

W celu transferu danych np. z Neo4j do Apache AGE należy wywołać następującą komendę:

```bash
>> python graph_converter.py -s neo4j -d age
```
