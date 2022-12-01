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
    data: list[list] = []
    for i in range(floor, ceil):
        points: set = generate_points(2**i, 0, 4000)
        for metric in ("Euclidiana", "Manhattan"):
            matrix: np.array = calculate_distance(points, metric)
            graph: nx.Graph = nx.from_numpy_array(matrix)

            # TODO: retornar espaço
            algorithms: list[str] = [
                "Twice Around The Tree",
                "Christofides",
                # "Branch And Bound",
            ]
            for algorithm in algorithms:
                row: list[int, str, str, float, float] = _measure_algorithm(
                    algorithm, graph, metric, i
                )
                data.append(row)
    return pd.DataFrame(
        data, columns=["Instância", "Algoritmo", "Distância", "Tempo", "Custo"]
    )


def _measure_algorithm(
    algorithm: str, graph: nx.Graph, metric: str, i: int
) -> list[int, str, str, float, float]:
    """Realiza a medição de um algoritmo em uma instância."""
    start: float = time.time()
    cost: float = tsp_solver(algorithm, graph)
    algorithm: str = algorithm
    end: float = time.time()
    diff_time: float = end - start
    return [i, algorithm, metric, diff_time, cost]
