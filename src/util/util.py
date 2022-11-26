"""Gere o conjunto de pontos e calcule as distâncias entre eles."""
from random import randint

import numpy as np
import scipy.spatial.distance as dist

from src.globals import MANHATTAN

FLOOR = 0
CEILING = 10
SIZE = CEILING - FLOOR + 1


def generator(number_of_points: int) -> set:
    """Gera uma lista de tamanho `number_of_points` de pontos aleatórios."""
    if number_of_points > SIZE * SIZE:
        raise Exception("Muitos pontos para pouco espaço!")

    points: set = set()

    while len(points) < number_of_points:
        x_coord = randint(FLOOR, CEILING)
        y_coord = randint(FLOOR, CEILING)
        point = (x_coord, y_coord)
        if point not in points:
            points.add(point)

    return points


def calculate_distance(points: set, distance: str) -> np.array:
    """Calcula as distâncias entre os `points` e as armazena numa matriz de adjacência."""
    size: int = len(points)
    adjacency_matrix: np.array = np.zeros((size, size))
    for i, p in enumerate(points):
        for j, q in enumerate(points):
            distance: float = (
                dist.cityblock(p, q) if distance == MANHATTAN else dist.euclidean(p, q)
            )
            adjacency_matrix[i][j] = distance
    return adjacency_matrix
