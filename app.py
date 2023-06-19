import json

import networkx as nx
from bson import json_util
from flask import Flask, jsonify
from flask_cors import CORS

from calculate_weight_function import calculate_weight
from dijkstra_algorithm import dijkstra

app = Flask(__name__)
CORS(app)   # Enable CORS


# Crear hashmap
nodes = {}
# Crear lista
nodes_lst = []


# Lectura del dataset en JSON
with open('data.json', 'r') as file:
    json_nodes = json.load(file)
    for node in json_nodes:
        # Eliminar el caracter ':' de los títulos de las películas y series
        # para evitar problemas con el algoritmo de Dijkstra
        node['Title'] = node['Title'].replace(':', ' ')
        # Agregarlos a la lista
        nodes_lst.append(node)
        # Agregar datos al hashmap
        nodes[node['Title']] = node


# Crear grafo
netflix_graph = nx.Graph()


# Agregar nodos
for node in nodes_lst:
    netflix_graph.add_node(str(node['Title']))


# Agregar ejes
try:
    # Si existe el archivo, agregar los ejes
    with open('edges.json', 'r') as file:
        edges = json.load(file)
        for edge in edges:
            netflix_graph.add_edge(
                edge['source'], edge['target'], weight=edge['weight'])
except FileNotFoundError:
    # Si no existe, crear el archivo y agregar los ejes
    edges = []
    for e, source in enumerate(nodes_lst):
        for i in range(e + 1, len(nodes_lst)):
            target = nodes_lst[i]
            weight = calculate_weight(source, target)
            if weight > 0:
                edges.append({
                    'source': str(source['Title']),
                    'target': str(target['Title']),
                    'weight': weight
                })
                netflix_graph.add_edge(str(source['Title']), str(
                    target['Title']), weight=weight)
    with open('edges.json', 'w') as file:
        json.dump(edges, file, indent=2)


@ app.route('/')
def home():
    # Total
    return jsonify([node['Title'] for node in nodes_lst])


@ app.route('/nodes')
def graph_nodes():
    """
    Nodos del grafo
    """
    return jsonify(nx.node_link_data(netflix_graph).get('nodes'))


@ app.route('/links')
def graph_links():
    """
    Aristas del grafo
    """
    return jsonify(nx.node_link_data(netflix_graph).get('links'))


@ app.route('/dijkstra/<string:start>/<string:end>',
            defaults={'type_film': 'both', 'runtime': 4, 'score': 0})
@ app.route('/dijkstra/<string:start>/<string:end>/<string:type_film>/<int:runtime>/<int:score>')
def dijkstra_route(start: str, end: str, type_film: str, runtime: int, score: int):
    """
    Camino mínimo entre dos nodos con el Algortimo Dijkstra
    Args:
        start (str) : Nodo origen
        end (str) : Nodo destino
        type_film (str) : Tipo de película (movie, series, both)
        runtime (int) : Duración de la película
        score (int) : Puntuación de la película
    Returns:
        path (list) : Lista de nodos que conforman el camino mínimo
        distance (int) : Distancia total del camino mínimo
    """
    path, dist = dijkstra(netflix_graph, start, end,
                          type_film, runtime, score, nodes)

    if len(path):
        return json.dumps({'path': path, 'distance': dist}, default=json_util.default)
    else:
        return json.dumps({'path': [], 'distance': 'Infinity'}, default=json_util.default)


@ app.route('/data')
def data():
    """
    Datos de las películas y series
    """
    return json.dumps({'nodes': nodes}, default=json_util.default)


@ app.route('/data/<string:title>')
def data_by_title(title: str):
    """
    Película o serie por título
    Args:
        title (str) : Título de la película o serie
    Returns:
        node (dict) : Datos de la película o serie
    """

    return json.dumps(nodes.get(str(title)), default=json_util.default)


if __name__ == '__main__':
    app.run(debug=True)
