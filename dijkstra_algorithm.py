import math
from queue import PriorityQueue

import networkx as nx


def filter_film(mynode: dict, type_film: str, runtime: int, score: int):
    runtime_dict = {
        '< 30 minutes': 1,
        '30-60 mins': 2,
        '1-2 hour': 3,
        '> 2 hrs': 4
    }

    if type_film == 'both' and runtime == 4 and score == 0:
        return True
    else:
        isValid = True

        if type_film != 'both' and mynode['Series or Movie'] != type_film:
            isValid = False
        if runtime != 4 and runtime_dict[mynode['Runtime']] > runtime:
            isValid = False
        if score != 0 and float(mynode['IMDb Score']) < score:
            isValid = False
        return isValid


def dijkstra(graph: 'nx.classes.graph.Graph', start: str, end: str, type_film: str, runtime: int, score: int, nodes):
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
    def backtrace(prev, start: str, end: str):
        node = end
        path = []
        while node != start:
            if prev[node] == None:
                return path
            path.append(node)
            node = prev[node]
        path.append(node)
        path.reverse()
        return path

    # Peso del eje
    def cost(u, v):
        if (u, v) not in graph.edges:
            return math.inf
        return graph[u][v]['weight']

    # Diccionario para los nodos previos
    prev = {v: None for v in graph}
    # Distancia entre los nodos (math.inf por defecto)
    dist = {v: math.inf for v in graph}
    # Set de los nodos visitados
    visited = set()
    # Cola de prioridad
    pq = PriorityQueue()

    dist[start] = 0
    pq.put((dist[start], start))

    while pq.qsize() != 0:
        # Obtener el último elemento de la cola de prioridad
        curr_cost, curr = pq.get()
        visited.add(curr)
        # Continuar si el grafo posee nodos
        if dict(graph.adjacency()).get(curr) is not None:
            # Obtener los nodos del grafo
            for neighbor in dict(graph.adjacency()).get(curr):
                # Buscar en el hashmap el nodo
                mynode = nodes[neighbor]
                if (filter_film(mynode, type_film, runtime, score)):
                    path = dist[curr] + cost(curr, neighbor)
                    # Si encontramos un camino más corto
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
