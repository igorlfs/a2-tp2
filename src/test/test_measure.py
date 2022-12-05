"""Testes do módulo `measure`."""
import networkx as nx
from pytest_mock import MockerFixture

from src.measure import measure_algorithm


def test_measure_algorithm(mocker: MockerFixture) -> None:
    """Teste medição dos dados dos algoritmos."""
    graph: nx.Graph = nx.Graph()
    mocker.patch("src.measure.measure.tsp_solver", return_value=10)
    data: list = measure_algorithm("Christofides", graph, "Euclidiana", 1)
    # Nós usamos o próprio tempo dos dados porque isso seria chato de estimar
    expected: list = [1, "Christofides", "Euclidiana", data[3], 10]
    assert data == expected
