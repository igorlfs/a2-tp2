"""Implementa os algoritmos para solução do caixeiro viajante."""
import networkx as nx

from src.util import calculate_cost


def twice_around_the_tree(graph: nx.Graph) -> float:
    """Aproxime o caixeiro viajante para `graph` usando o `twice_around_the_tree`."""
    mst: nx.Graph = nx.minimum_spanning_tree(graph)
    vertex_list: list[int] = list(nx.dfs_preorder_nodes(mst, 0))
    return calculate_cost(vertex_list, graph)
