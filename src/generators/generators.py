"""Gere a instância e seu conjunto de pontos."""
import time
from random import randint

import networkx as nx
import numpy as np
import pandas as pd

from src.algorithms import christofides, twice_around_the_tree
from src.calculate import calculate_distance

COORDINATES_FLOOR = 0
COORDINATES_CEIL = 10000
SIZE = COORDINATES_CEIL - COORDINATES_FLOOR + 1


INSTANCE_FLOOR = 4
INSTANCE_CEIL = 11  # O método range é exclusivo em relação ao teto


def generate_points(number_of_points: int) -> set:
    """Gera uma lista de tamanho `number_of_points` de pontos aleatórios."""
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
    for i in range(INSTANCE_FLOOR, INSTANCE_CEIL):
        points: set = generate_points(2**i)
        for j in (True, False):
            matrix: np.array = calculate_distance(points, j)
            graph: nx.Graph = nx.from_numpy_array(matrix)

            dist_type: str = "Euclidiana" if j else "Manhattan"

            # TODO: retornar espaço
            start: float = time.time()
            cost: float = twice_around_the_tree(graph)
            end: float = time.time()
            diff_time: float = end - start
            df = pd.concat(
                [
                    pd.DataFrame(
                        [[i, "Twice Around The Tree", dist_type, diff_time, cost]],
                        columns=df.columns,
                    ),
                    df,
                ],
                ignore_index=True,
            )

            start: float = time.time()
            cost: float = christofides(graph)
            end: float = time.time()
            diff_time: float = end - start
            df = pd.concat(
                [
                    pd.DataFrame(
                        [[i, "Christofides", dist_type, diff_time, cost]],
                        columns=df.columns,
                    ),
                    df,
                ],
                ignore_index=True,
            )
    return df
