"""Funções de estimadores do Branch And Bound."""
from math import ceil, inf

import networkx as nx

from src.algorithms.node import Node


def initial_bound(graph: nx.Graph) -> tuple[float, list[tuple[float, float, bool]]]:
    """
    Calcula um limite inferior para o TSP de `graph`.

    Também retorne uma lista de tuplas com os
    """
    size: int = graph.number_of_nodes()
    boundary: float = 0
    min_weights: list[tuple[float, float, bool]] = []
    for i in range(size):
        smallest: tuple[float, float] = (inf, inf, False)
        for j in range(size):
            if i == j:
                continue
            weight: float = graph[i][j]["weight"]
            if weight < smallest[0]:
                smallest = (weight, smallest[0], False)
            elif weight < smallest[1]:
                smallest = (smallest[0], weight, False)
        min_weights.append(smallest)
        boundary += smallest[0] + smallest[1]
    return ceil(boundary) / 2, min_weights


def update_bound(
    graph: nx.Graph, v: int, node: Node
) -> tuple[float, list[tuple[float, float, bool]]]:
    """Atualiza limite inferior após adicionar um vértice `v` na solução de `node`."""
    u: int = node.sol[-1]
    if not graph.has_edge(u, v):
        return inf, []
    weight: float = graph[u][v]["weight"]
    min_weights: list[tuple[float, float, bool]] = node.weights.copy()
    min_weights[u], increment = _update_bound_helper(weight, min_weights[u])
    min_weights[v], other_increment = _update_bound_helper(weight, min_weights[v])
    increment += other_increment
    boundary: float = node.boundary + ceil(increment / 2)
    return boundary, min_weights


def _update_bound_helper(
    weight: float, index_min: tuple[float, float, bool]
) -> tuple[tuple[float, float, bool], float]:
    increment: float = 0
    if weight > index_min[0]:
        if not index_min[2]:
            increment += weight - index_min[1]
            index_min = (index_min[0], weight, True)
        else:
            increment += weight - index_min[0]
    return index_min, increment
