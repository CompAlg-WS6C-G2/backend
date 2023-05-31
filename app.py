import json

import networkx as nx
from bson import json_util
from flask import Flask, jsonify
from pymongo import MongoClient

from calculate_weight_function import calculate_weight
from dijkstra_algorithm import dijkstra

app = Flask(__name__)

# Obtener datos de MongoDB
client = MongoClient(
    'mongodb+srv://lepian:tCJRUEhEhRy5YXma@compalg-ws6c-g2.uwf4hxj.mongodb.net/?retryWrites=true&w=majority')
db = client['data']

nodes = list(db['film'].find())

for node in nodes:
    node['Title'] = node['Title'].replace(':', ' ')

netflix_graph = nx.DiGraph()

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
def test():
    return lst_nodes_graph


@app.route('/dijkstra/<string:start>/<string:end>')
def dijkstra_route(start: str, end: str):
    path, dist = dijkstra(netflix_graph, start, end)

    return json.dumps({'path': path, 'distance': dist}, default=json_util.default)


@app.route('/film-title')
def netflixList():
    films = []
    for i in nodes:
        films.append(i['Title'])
    _films = list()
    for i in set(films):
        temp_dict = dict()
        temp_dict["Film"] = i
        _films.append(temp_dict)
    return jsonify(_films)


@app.route('/nodes')
def index():
    return json.dumps({'nodes': nodes}, default=json_util.default)


if __name__ == '__main__':
    app.run(debug=True)
