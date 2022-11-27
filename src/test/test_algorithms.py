"""Testes simples para os algoritmos implementados."""
import networkx as nx
import networkx.algorithms.approximation as nx_app
import numpy as np
import pytest
from numpy.testing import assert_almost_equal

from src.algorithms import tsp_matcher, tsp_solver
from src.calculate import calculate_cost, calculate_distance
from src.generators import generate_points


def test_twice_around_the_tree() -> None:
    """Teste o twice around the tree usando o exemplo das aulas."""
    matrix: np.array = np.array(
        [
            [0, 0, 0, 0, 0],
            [4, 0, 0, 0, 0],
            [8, 6, 0, 0, 0],
            [9, 8, 10, 0, 0],
            [12, 9, 11, 7, 0],
        ]
    )

    graph: nx.Graph = nx.from_numpy_array(matrix)
    cost: float = tsp_solver(1, graph)

    assert cost == 39


def test_christofides() -> None:
    """
    Compare o resultado com a implementação do networkx.

    Exemplo: https://en.wikipedia.org/wiki/File:Weighted_K4.svg
    """
    matrix: np.array = np.array(
        [
            [0, 0, 0, 0],
            [20, 0, 0, 0],
            [42, 30, 0, 0],
            [35, 35, 12, 0],
        ]
    )
    graph: nx.Graph = nx.from_numpy_array(matrix)

    expected_cycle: list[int] = nx_app.christofides(graph)

    expected_cost: float = calculate_cost(expected_cycle, graph)

    actual_cost: float = tsp_solver(2, graph)

    assert expected_cost == actual_cost


def test_christofides_complex() -> None:
    """Gere uma matriz usando as funções do programa e compare ambas implementações."""
    points = generate_points(6)
    matrix = calculate_distance(points, True)
    graph: nx.Graph = nx.from_numpy_array(matrix)
    expected_cycle: list[int] = nx_app.christofides(graph)
    expected_cost: float = calculate_cost(expected_cycle, graph)
    actual_cost: float = tsp_solver(2, graph)

    assert_almost_equal(actual_cost, expected_cost)


def test_tsp_solver_exception() -> None:
    """Capture exceções de tsp_solver e tsp_matcher."""
    graph: nx.Graph = nx.Graph()
    with pytest.raises(Exception, match="Esse algoritmo não existe"):
        tsp_solver(4, graph)
    with pytest.raises(Exception, match="Esse algoritmo não existe"):
        tsp_matcher(4)
