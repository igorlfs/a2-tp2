"""Testes simples para os algoritmos implementados."""
import networkx as nx
import numpy as np

from src.algorithms import twice_around_the_tree


def test_twice_around_the_tree() -> None:
    """Teste o twice around the tree usando o exemplo das aulas."""
    matrix = np.array(
        [
            [0, 0, 0, 0, 0],
            [4, 0, 0, 0, 0],
            [8, 6, 0, 0, 0],
            [9, 8, 10, 0, 0],
            [12, 9, 11, 7, 0],
        ]
    )

    my_graph = nx.from_numpy_array(matrix)
    cost = twice_around_the_tree(my_graph)

    assert cost == 39
