"""Testes para algumas propriedades dos geradores."""

import networkx as nx
import pytest
from pytest_mock import MockerFixture

from src.generators import measure_algorithm, generate_points


def test_generate_points_exception() -> None:
    """Capture exceções de generate_points."""
    with pytest.raises(Exception, match="Muitos pontos para pouco espaço!"):
        generate_points(10, 1, 2)


def test__measure_algorithm(mocker: MockerFixture) -> None:
    """Teste medição dos dados dos algoritmos."""
    graph: nx.Graph = nx.Graph()
    mocker.patch("src.generators.generators.tsp_solver", return_value=10)
    data: list = measure_algorithm("Christofides", graph, "Euclidiana", 1)
    # Nós usamos o próprio tempo dos dados porque isso seria chato de estimar
    expected: list = [1, "Christofides", "Euclidiana", data[3], 10]
    assert data == expected
