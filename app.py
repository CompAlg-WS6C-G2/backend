import json

import networkx as nx
from bson import json_util
from flask import Flask, jsonify
from pymongo import MongoClient

from dijkstra_algorithm import dijkstra
from calculate_weight_function import calculate_weight

app = Flask(__name__)

# Obtener datos de MongoDB
client = MongoClient(
    'mongodb+srv://lepian:tCJRUEhEhRy5YXma@compalg-ws6c-g2.uwf4hxj.mongodb.net/?retryWrites=true&w=majority')
db = client['data']

nodes = list(db['film'].find())

netflix_graph = nx.DiGraph()

for e, node in enumerate(nodes):
    for i in range(e + 1, 20):
        target = nodes[i]
        weight = calculate_weight(node, target)
        if weight > 0:
            netflix_graph.add_edge(str(node['Title'].replace(':', '')), str(
                target['Title'].replace(':', '')), weight=weight)
        else:
            netflix_graph.add_node(str(node['Title'].replace(':', '')))
    if e == 20:
        break

@app.route('/dijkstra/<string:start>/<string:end>')
def dijkstra_route(start, end):
    print("hola")
    #run dijkstra
    path, dist = dijkstra(netflix_graph, start, end)
    #get nodes and links necesary to show the path
    _nodes = []
    for node in path:
        _nodes.append(nodes[node-1])

    #return the path
    return json.dumps({'nodes': _nodes, 'distance': dist}, default=json_util.default)

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
