"""Gere a instância e seu conjunto de pontos."""
import time
from random import randint

import networkx as nx
import numpy as np
import pandas as pd

from src.algorithms import tsp_solver
from src.calculate import calculate_distance


def generate_points(number_of_points: int, floor: int, ceil: int) -> set:
    """Gera um conjunto de tamanho `number_of_points` de pontos aleatórios."""
    size: int = ceil - floor + 1
    if number_of_points > size * size:
        raise Exception("Muitos pontos para pouco espaço!")

    points: set[tuple[int, int]] = set()

    while len(points) < number_of_points:
        x_coord: int = randint(floor, ceil)
        y_coord: int = randint(floor, ceil)
        point: tuple[int, int] = (x_coord, y_coord)
        if point not in points:
            points.add(point)

    return points


def generate_instances(size: int, metric: str) -> pd.DataFrame:
    """Gere instâncias do problema do caixeiro viajante."""
    points: set[tuple[int, int]] = generate_points(2**size, 0, 4000)
    matrix: np.array = calculate_distance(points, metric)
    graph: nx.Graph = nx.from_numpy_array(matrix)
    return graph


def measure_algorithm(algorithm: str, graph: nx.Graph, metric: str, i: int) -> list:
    """Executa um algoritmo em uma instância e retorna suas métricas."""
    start: float = time.time()
    cost: float = tsp_solver(algorithm, graph)
    algorithm: str = algorithm
    end: float = time.time()
    diff_time: float = end - start
    return [i, algorithm, metric, diff_time, cost]
