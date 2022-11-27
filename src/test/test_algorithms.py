"""Testes simples para os algoritmos implementados."""
import networkx as nx
import networkx.algorithms.approximation as nx_app
import numpy as np

from src.algorithms import tsp_solver


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


def get_networx_christofides_cost(graph: nx.Graph) -> float:
    """Calcule o custo do TSP pela implementação do Christofides do networkx."""
    cycle: list[tuple[int, int]] = nx_app.christofides(graph)
    edge_list: list = list(nx.utils.pairwise(cycle))
    expected_cost = 0
    for edge in edge_list:
        expected_cost += graph[edge[0]][edge[1]]["weight"]
    return expected_cost


def test_christofides() -> None:
    """
    Compare o resultado com a implementação do networkx.

    Exemplo: https://en.wikipedia.org/wiki/Christofides_algorithm#Example
    """
    matrix: np.array = np.array(
        [
            [0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0],
            [1, 1, 0, 0, 0],
            [1, 1, 2, 0, 0],
            [1, 2, 1, 1, 0],
        ]
    )
    graph: nx.Graph = nx.from_numpy_array(matrix)

    expected_cost: float = get_networx_christofides_cost(graph)

    actual_cost: float = tsp_solver(2, graph)

    assert expected_cost == actual_cost


def test_christofides_pt2() -> None:
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

    expected_cost: float = get_networx_christofides_cost(graph)

    actual_cost: float = tsp_solver(2, graph)

    assert expected_cost == actual_cost
