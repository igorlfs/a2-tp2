"""Calcule distância e custos."""

import networkx as nx
import numpy as np
import scipy.spatial.distance as dist


def calculate_distance(points: set, euclidean: bool) -> np.array:
    """Calcula as distâncias entre os `points` e as armazena numa matriz de adjacência."""
    size: int = len(points)
    adjacency_matrix: np.array = np.zeros((size, size))
    for i, p in enumerate(points):
        for j, q in enumerate(points):
            distance: float = dist.euclidean(p, q) if euclidean else dist.cityblock(p, q)
            adjacency_matrix[i][j] = distance
    return adjacency_matrix


def calculate_cost(cycle: list[int], graph: nx.Graph) -> float:
    """Calcula o custo de se percorrer o ciclo `cycle` em `graph`."""
    cost: float = 0
    for i in range(0, len(cycle) - 1):
        cost += graph[cycle[i]][cycle[i + 1]]["weight"]
    return cost
