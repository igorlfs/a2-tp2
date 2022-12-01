"""Calcule distância e custo de se percorrer um ciclo em um grafo."""

import networkx as nx
import numpy as np
import scipy.spatial.distance as dist


def calculate_distance(points: set[tuple[int, int]], metric: str) -> np.array:
    """
    Calcula as distâncias entre os `points` e as armazena numa matriz de adjacência.

    Use `euclidean` para decidir se a distância é euclidiana ou de Manhattan.
    """
    size: int = len(points)
    adjacency_matrix: np.array = np.zeros((size, size))
    for i, p in enumerate(points):
        for j, q in enumerate(points):
            if j >= i:
                continue
            distance: float = 0
            match metric:  # noqa: E999
                case "Euclidiana":
                    distance += dist.euclidean(p, q)
                case "Manhattan":
                    distance += dist.cityblock(p, q)
                case _:
                    raise Exception(f"Métrica de distância {metric} desconhecida")
            adjacency_matrix[i][j] = distance
    return adjacency_matrix


def calculate_cost(cycle: list[int], graph: nx.Graph) -> float:
    """Calcula o custo de se percorrer o ciclo `cycle` em `graph`."""
    cost: float = 0
    for i in range(0, len(cycle) - 1):
        cost += graph[cycle[i]][cycle[i + 1]]["weight"]
    return cost
