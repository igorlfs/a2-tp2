"""Abstrai a implementação dos algoritmos para solução do TSP."""
import networkx as nx

from src.algorithms import christofides, twice_around_the_tree


def tsp_solver(i: int, graph: nx.Graph) -> float:
    """Enumera as soluções para o TSP."""
    match i:  # noqa (ruff não suporta match)
        case 1:
            return twice_around_the_tree(graph)
        case 2:
            return christofides(graph)
        case _:
            raise Exception("Esse algoritmo não existe")


def tsp_matcher(i: int) -> str:
    """Case um identificador de algoritmo com seu nome."""
    match i:
        case 1:
            return "Twice Around The Tree"
        case 2:
            return "Christofides"
        case _:
            raise Exception("Esse algoritmo não existe")
