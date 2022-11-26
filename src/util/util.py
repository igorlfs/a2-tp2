"""Gere o conjunto de pontos e calcule as distâncias entre eles."""
import time
from random import randint

import networkx as nx
import numpy as np
import pandas as pd
import scipy.spatial.distance as dist

from src.algorithms import twice_around_the_tree

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

            # 4.1 Retornar tempo, espaço, qualidade da solução
            start: float = time.time()
            cost: float = twice_around_the_tree(graph)
            end: float = time.time()
            diff_time: float = end - start
            dist_type: str = "Euclidiana" if j else "Manhattan"
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

    return df
