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
    size = ceil - floor + 1
    if number_of_points > size * size:
        raise Exception("Muitos pontos para pouco espaço!")

    points: set = set()

    while len(points) < number_of_points:
        x_coord: int = randint(floor, ceil)
        y_coord: int = randint(floor, ceil)
        point: tuple[int, int] = (x_coord, y_coord)
        if point not in points:
            points.add(point)

    return points


def generate_instances(floor: int, ceil: int) -> pd.DataFrame:
    """Gere instâncias, rode os algoritmos e colete as métricas."""
    df: pd.DataFrame = pd.DataFrame(
        columns=["Instância", "Algoritmo", "Distância", "Tempo", "Custo"]
    )
    for i in range(floor, ceil):
        points: set = generate_points(2**i, 0, 4000)
        for j in (True, False):
            matrix: np.array = calculate_distance(points, j)
            graph: nx.Graph = nx.from_numpy_array(matrix)

            # TODO: retornar espaço
            algorithms: list[str] = [
                "Twice Around The Tree",
                "Christofides",
                "Branch And Bound",
            ]
            for k in algorithms:
                _measure_algorithm(k, graph, df, j, i)
    return df


def _measure_algorithm(
    k: int, graph: nx.Graph, df: pd.DataFrame, j: bool, i: int
) -> None:
    """Realiza a medição de um algoritmo em uma instância."""
    dist_type: str = "Euclidiana" if j else "Manhattan"
    start: float = time.time()
    cost: float = tsp_solver(k, graph)
    algorithm: str = k
    end: float = time.time()
    diff_time: float = end - start
    df.loc[len(df)] = [i, algorithm, dist_type, diff_time, cost]
