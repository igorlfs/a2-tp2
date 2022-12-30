"""Abstrai a implementação dos algoritmos para solução do TSP."""
import networkx as nx

from src.algorithms import branch_and_bound, christofides, twice_around_the_tree


def tsp_solver(algorithm: str, graph: nx.Graph) -> float:
    """Enumera as soluções para o TSP."""
    match algorithm:  # noqa: E999 (ruff não suporta match)
        case "Twice Around The Tree":
            return twice_around_the_tree(graph)
        case "Christofides":
            return christofides(graph)
        case "Branch And Bound":
            return branch_and_bound(graph)
        case _:
            raise Exception("Esse algoritmo não existe")
