"""Testes para algumas propriedades dos calculadores."""

from math import sqrt

import networkx as nx
import numpy as np
import pytest

from src.calculate import calculate_cost, calculate_distance


def test_calculate_distance() -> None:
    """Teste distâncias euclidiana e Manhattan."""
    points: set[tuple[int, int]] = {(0, 0), (1, 1)}
    dist_euclidean: float = calculate_distance(points, "Euclidiana")[1][0]
    assert dist_euclidean == sqrt(2)
    dist_manhattan: float = calculate_distance(points, "Manhattan")[1][0]
    assert dist_manhattan == 2


def test_calculate_distance_exception() -> None:
    """Teste distâncias inexistentes."""
    points: set[tuple[int, int]] = {(0, 0), (1, 1)}
    with pytest.raises(Exception, match="Métrica de distância PT desconhecida"):
        calculate_distance(points, "PT")


def test_calculate_cost() -> None:
    """Teste cálculo de custo de um ciclo."""
    matrix: np.ndarray = np.array(
        [
            [0, 0, 0, 0],
            [20, 0, 0, 0],
            [42, 30, 0, 0],
            [35, 35, 12, 0],
        ]
    )
    graph: nx.Graph = nx.from_numpy_array(matrix)
    cycle: list[int] = [0, 3, 2, 1, 0]
    cost = calculate_cost(cycle, graph)

    assert cost == 97
