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


def calculate_cost(vertices: list[int], graph: nx.Graph) -> float:
    """Calcula o custo de percorrer o caminho `vertices` em `graph`."""
    cost: float = 0
    size: int = len(vertices)
    for i in vertices:
        cost += graph[i % size][(i + 1) % size]["weight"]
    return cost
