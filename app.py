import json

import networkx as nx
from bson import json_util
from flask import Flask, jsonify
from flask_cors import CORS

from calculate_weight_function import calculate_weight
from dijkstra_algorithm import dijkstra

app = Flask(__name__)
CORS(app)   # Enable CORS


with open ('data.json') as f:
    nodes = json.load(f)

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
    return lst_nodes_graph


@app.route('/links')
def graph_links():
    return jsonify(nx.node_link_data(netflix_graph).get('links'))


@app.route('/nodes')
def graph_nodes():
    return jsonify(nx.node_link_data(netflix_graph).get('nodes'))


@app.route('/dijkstra/<string:start>/<string:end>')
def dijkstra_route(start: str, end: str):
    path, dist = dijkstra(netflix_graph, start, end)

    return json.dumps({'path': path, 'distance': dist}, default=json_util.default)


@app.route('/mongodb_nodes')
def mongodb_data():
    return json.dumps({'nodes': nodes}, default=json_util.default)


if __name__ == '__main__':
    app.run(debug=True)
