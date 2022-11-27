"""Gere a instância e seu conjunto de pontos."""
import time
from random import randint

import networkx as nx
import numpy as np
import pandas as pd

from src.algorithms import tsp_matcher, tsp_solver
from src.calculate import calculate_distance

COORDINATES_FLOOR = 0
COORDINATES_CEIL = 10000
SIZE = COORDINATES_CEIL - COORDINATES_FLOOR + 1


INSTANCE_FLOOR = 4
INSTANCE_CEIL = 11  # O método range é exclusivo em relação ao teto


def generate_points(number_of_points: int) -> set:
    """Gera um conjunto de tamanho `number_of_points` de pontos aleatórios."""
    if number_of_points > SIZE * SIZE:
        raise Exception("Muitos pontos para pouco espaço!")

    points: set = set()

    while len(points) < number_of_points:
        x_coord: int = randint(COORDINATES_FLOOR, COORDINATES_CEIL)
        y_coord: int = randint(COORDINATES_FLOOR, COORDINATES_CEIL)
        point: tuple[int, int] = (x_coord, y_coord)
        if point not in points:
            points.add(point)

    return points


def generate_instances() -> pd.DataFrame:
    """Gere instâncias, rode os algoritmos e colete as métricas."""
    df: pd.DataFrame = pd.DataFrame(
        columns=["Instância", "Algoritmo", "Distância", "Tempo", "Custo"]
    )
    for i in range(INSTANCE_FLOOR, 8):
        points: set = generate_points(2**i)
        for j in (True, False):
            matrix: np.array = calculate_distance(points, j)
            graph: nx.Graph = nx.from_numpy_array(matrix)

            # TODO: retornar espaço
            for k in range(1, 3):
                measure_algorithm(k, graph, df, j, i)
    return df


def measure_algorithm(k: int, graph: nx.Graph, df: pd.DataFrame, j: int, i: int) -> None:
    """Realiza a medição de um algoritmo em uma instância."""
    dist_type: str = "Euclidiana" if j else "Manhattan"
    start: float = time.time()
    cost: float = tsp_solver(k, graph)
    algorithm: str = tsp_matcher(k)
    end: float = time.time()
    diff_time: float = end - start
    df.loc[len(df)] = [i, algorithm, dist_type, diff_time, cost]
