import math
from queue import PriorityQueue

import networkx as nx


def dijkstra(graph: 'nx.classes.graph.Graph', start: str, end: str) -> 'List':
    """
    Algoritmo Dijkstra para encontrar el camino más corto entre dos nodos

    Args:
        graph (networkx.classes.graph.Graph): Grafo
        start (str): Nodo inicio
        end (str): Nodo objetivo

    Returns:
        backtrace ([]): Camino mínimo del Nodo inicio al Nodo fin
        dist[end] (int) : Distancia hacia el Nodo fin
    """

    # Menor camino de nodo_inicio a nodo_objetivo
    def backtrace(prev, start, end):
        node = end
        path = []
        while node != start:
            path.append(node)
            node = prev[node]
        path.append(node)
        path.reverse()
        return path

    # Peso del eje
    def cost(u, v):
        return graph.get_edge_data(u, v).get('weight')

    # Diccionario para los nodos previos
    prev = {}
    # Distancia entre los nodos (math.inf por defecto)
    dist = {v: math.inf for v in list(nx.nodes(graph))}
    # Set de los nodos visitados
    visited = set()
    # Cola de prioridad
    pq = PriorityQueue()

    dist[start] = 0
    pq.put((dist[start], start))

    while 0 != pq.qsize():
        curr_cost, curr = pq.get()
        visited.add(curr)
        # Mirar los nodos adyacentes al actual
        if dict(graph.adjacency()).get(curr) is not None:
            for neighbor in dict(graph.adjacency()).get(curr):
                # Si encontramos un camino más corto
                path = dist[curr] + cost(curr, neighbor)
                if path < dist[neighbor]:
                    # Actualizamos la distancia si encontramos una más corta
                    dist[neighbor] = path
                    # Actualizamos el nodo previo para ser el nodo previo en el nuevo
                    # camino mínimo
                    prev[neighbor] = curr
                    # Si no hemos visitado al nodo vecino (adyacente)
                    if neighbor not in visited:
                        # Marcar el nodo como visitado
                        visited.add(neighbor)
                        # Insertar en la cola de prioridad
                        pq.put((dist[neighbor], neighbor))
                    # De otra manera, actualizar la entrada en la cola de prioridad
                    else:
                        # Remover anterior
                        _ = pq.get((dist[neighbor], neighbor))
                        # Insertar nuevo
                        pq.put((dist[neighbor], neighbor))

    return backtrace(prev, start, end), dist[end]
