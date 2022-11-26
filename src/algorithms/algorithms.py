import networkx as nx

from src.util import calculate_cost


def twice_around_the_tree(graph: nx.Graph) -> float:
    mst: nx.Graph = nx.minimum_spanning_tree(graph)
    vertex_list: list[int] = list(nx.dfs_preorder_nodes(mst, 0))
    return calculate_cost(vertex_list, graph)
