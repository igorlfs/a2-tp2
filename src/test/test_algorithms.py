"""Testes simples para os algoritmos implementados."""
import networkx as nx
import networkx.algorithms.approximation as nx_app
import numpy as np
import pytest
from numpy.testing import assert_almost_equal

from src.algorithms import tsp_solver
from src.algorithms.bounds import initial_bound, update_bound
from src.algorithms.node import Node
from src.calculate import calculate_cost
from src.generators import generate_instances


def test_twice_around_the_tree() -> None:
    """Teste o twice around the tree usando o exemplo das aulas."""
    matrix: np.ndarray = np.array(
        [
            [0, 0, 0, 0, 0],
            [4, 0, 0, 0, 0],
            [8, 6, 0, 0, 0],
            [9, 8, 10, 0, 0],
            [12, 9, 11, 7, 0],
        ]
    )
    graph: nx.Graph = nx.from_numpy_array(matrix)
    cost: float = tsp_solver("Twice Around The Tree", graph)

    assert cost == 39


@pytest.fixture
def _input_graph() -> nx.Graph:
    matrix: np.ndarray = np.array(
        [
            [0, 0, 0, 0],
            [20, 0, 0, 0],
            [42, 30, 0, 0],
            [35, 34, 12, 0],
        ]
    )
    graph: nx.Graph = nx.from_numpy_array(matrix)
    return graph


def test_christofides(_input_graph: nx.Graph) -> None:
    """
    Compare o resultado com a implementação do networkx.

    Exemplo: https://en.wikipedia.org/wiki/File:Weighted_K4.svg
    """
    expected_cycle: list[int] = nx_app.christofides(_input_graph)
    expected_cost: float = calculate_cost(expected_cycle, _input_graph)
    actual_cost: float = tsp_solver("Christofides", _input_graph)

    assert expected_cost == actual_cost


def test_christofides_complex() -> None:
    """Gere uma matriz usando as funções do programa e compare ambas implementações."""
    graph: nx.Graph = generate_instances(7, "Euclidiana")
    expected_cycle: list[int] = nx_app.christofides(graph)
    expected_cost: float = calculate_cost(expected_cycle, graph)
    actual_cost: float = tsp_solver("Christofides", graph)

    assert_almost_equal(actual_cost, expected_cost)


def test_tsp_solver_exception() -> None:
    """Capture exceções de tsp_solver."""
    graph: nx.Graph = nx.Graph()
    with pytest.raises(Exception, match="Esse algoritmo não existe"):
        tsp_solver("Lula 13", graph)


@pytest.fixture
def _input_graph_bound() -> nx.Graph:
    matrix: np.ndarray = np.array(
        [
            [0, 0, 0, 0, 0],
            [3, 0, 0, 0, 0],
            [1, 6, 0, 0, 0],
            [5, 7, 4, 0, 0],
            [8, 9, 2, 3, 0],
        ]
    )
    graph: nx.Graph = nx.from_numpy_array(matrix)
    return graph


def test_initial_bound(_input_graph_bound: nx.Graph) -> None:
    """Teste o bound usando o exemplo das aulas."""
    boundary, weights = initial_bound(_input_graph_bound)

    assert boundary == 14
    assert weights == [
        (1, 3, False),
        (3, 6, False),
        (1, 2, False),
        (3, 4, False),
        (2, 3, False),
    ]


def test_update_bound(_input_graph_bound: nx.Graph) -> None:
    """Teste o bound usando o exemplo das aulas."""
    init_cost, init_weights = initial_bound(_input_graph_bound)
    init_node: Node = Node(init_cost, 0, 0, [0], init_weights)

    # Legenda
    # Menor: menor dos dois menores pesos de arestas de um nó
    # Maior: MAIOR dos dois maiores pesos de arestas de um nó
    # Gigante: outros pesos de arestas

    # Tente reaproveitar instâncias
    # (é meio complicado se certificar que os parâmetros estão corretos)

    # Gigante
    boundary, weights = update_bound(_input_graph_bound, 3, init_node)
    assert boundary == 16
    # Gigante, Gigante
    node: Node = Node(16, 0, 0, [3, 0], weights)
    boundary, _ = update_bound(_input_graph_bound, 4, node)
    assert boundary == 22

    # Menor
    boundary, weights = update_bound(_input_graph_bound, 2, init_node)
    assert boundary == init_cost
    # Menor, Gigante
    node = Node(init_cost, 0, 0, [2, 0], weights)
    boundary, _ = update_bound(_input_graph_bound, 3, node)
    assert boundary == 16

    # Maior
    boundary, weights = update_bound(_input_graph_bound, 1, init_node)
    assert boundary == init_cost
    # Maior, Gigante
    node = Node(init_cost, 0, 0, [1, 0], weights)
    boundary, _ = update_bound(_input_graph_bound, 3, node)
    assert boundary == 17

    # Menor, Maior
    new_node: Node = Node(init_cost, 0, 0, [2], init_weights)
    _, weights = update_bound(_input_graph_bound, 0, new_node)
    node = Node(init_cost, 0, 0, [2, 0], weights)
    boundary, _ = update_bound(_input_graph_bound, 1, node)
    assert boundary == init_cost


def test_branch_and_bound(_input_graph: nx.Graph) -> None:
    """Teste o branch and bound usando o exemplo das aulas."""
    actual_cost: float = tsp_solver("Branch And Bound", _input_graph)
    assert actual_cost == 97


def test_branch_and_bound_complex() -> None:
    """Compara minha implementação com a do networkx, que é aproximativa."""
    graph: nx.Graph = generate_instances(3, "Euclidiana")
    expected_cycle: list[int] = nx_app.traveling_salesman_problem(graph)
    expected_cost: float = calculate_cost(expected_cycle, graph)
    actual_cost: float = tsp_solver("Branch And Bound", graph)

    assert_almost_equal(actual_cost, expected_cost)
