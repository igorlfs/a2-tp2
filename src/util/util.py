"""
Gere o conjunto de pontos e calcule as distâncias entre eles.
"""

from random import randint

import numpy as np
import scipy.spatial.distance as dist
from numba import njit

from src.globals import MANHATTAN

FLOOR = 0
CEILING = 10


@njit
def generator(number_of_points: int) -> np.array:
    """
    Gera uma lista de tamanho `number_of_points` de pontos aleatórios.
    """
    points: np.array = np.zeros((number_of_points, 2), dtype=np.int32)
    for i in range(number_of_points):
        points[i][0] = randint(FLOOR, CEILING)
        points[i][1] = randint(FLOOR, CEILING)
    return points


def calculate_distance(points: np.array, distance: str) -> np.array:
    """
    Calcula as distâncias entre os `points` e as armazena numa matriz de adjacência.
    """
    size: int = np.size(points, axis=0)
    adjacency_matrix: np.array = np.zeros((size, size))
    for i in range(size):
        for j in range(i):
            distance: float = (
                dist.cityblock(points[i], points[j])
                if distance == MANHATTAN
                else dist.euclidean(points[i], points[j])
            )
            adjacency_matrix[i][j] = distance
    return adjacency_matrix
