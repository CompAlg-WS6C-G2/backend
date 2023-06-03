import json

import networkx as nx
from bson import json_util
from flask import Flask, jsonify
from flask_cors import CORS
from pymongo import MongoClient

from calculate_weight_function import calculate_weight
from dijkstra_algorithm import dijkstra

app = Flask(__name__)
CORS(app)   # Enable CORS


# Obtener datos de MongoDB
client = MongoClient(
    'mongodb+srv://lepian:tCJRUEhEhRy5YXma@compalg-ws6c-g2.uwf4hxj.mongodb.net/?retryWrites=true&w=majority')
db = client['data']

nodes = list(db['film'].find())
for node in nodes:
    node['Title'] = node['Title'].replace(':', ' ')

netflix_graph = nx.Graph()

for e, node in enumerate(nodes):
    for i in range(e + 1, 21):
        target = nodes[i]
        weight = calculate_weight(node, target)
        if weight > 0:
            netflix_graph.add_edge(str(node['Title']), str(
                target['Title']), weight=weight)
        else:
            netflix_graph.add_node(str(node['Title']))
    if e == 20:
        break

lst_nodes_graph = list(netflix_graph.nodes)


@app.route('/')
def home():
    """
    Lista de los nombres de las películas y series
    """
    return lst_nodes_graph


@app.route('/links')
def graph_links():
    """
    Aristas del grafo
    """
    return jsonify(nx.node_link_data(netflix_graph).get('links'))


@app.route('/nodes')
def graph_nodes():
    """
    Nodos del grafo
    """
    return jsonify(nx.node_link_data(netflix_graph).get('nodes'))


@app.route('/dijkstra/<string:start>/<string:end>')
def dijkstra_route(start: str, end: str):
    """
    Camino mínimo entre dos nodos con el Algortimo Dijkstra
    Args:
        start (str) : Nodo origen
        end (str) : Nodo destino
    Returns:
        path (list) : Lista de nodos que conforman el camino mínimo
        distance (int) : Distancia total del camino mínimo
    """
    path, dist = dijkstra(netflix_graph, start, end)

    return json.dumps({'path': path, 'distance': dist}, default=json_util.default)


@app.route('/mongodb_nodes')
def mongodb_data():
    """
    Datos de las películas y series en MongoDB
    """
    return json.dumps({'nodes': nodes}, default=json_util.default)


@app.route('/mongodb_nodes/<string:title>')
def mongodb_data_by_title(title: str):
    """
    Película o serie en MongoDB por título
    Args:
        title (str) : Título de la película o serie
    Returns:
        node (dict) : Datos de la película o serie
    """
    return json.dumps(db['film'].find_one({'Title': title}), default=json_util.default)


if __name__ == '__main__':
    app.run(debug=True)
