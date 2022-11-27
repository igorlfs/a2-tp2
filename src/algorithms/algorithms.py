"""Implementa os algoritmos para solução do caixeiro viajante."""
import networkx as nx

from src.calculate import calculate_cost


def twice_around_the_tree(graph: nx.Graph) -> float:
    """Aproxime o caixeiro viajante para `graph` usando o `twice_around_the_tree`."""
    mst: nx.Graph = nx.minimum_spanning_tree(graph)
    cycle: list[int] = list(nx.dfs_preorder_nodes(mst, 0))
    cycle.append(0)
    return calculate_cost(cycle, graph)


def christofides(graph: nx.Graph) -> float:
    """Aproxime o caixeiro viajante para `graph` usando o algoritmo de `christofides`."""
    mst: nx.Graph = nx.minimum_spanning_tree(graph)
    odd_degree_vertices: list[int] = [node for (node, val) in mst.degree if val % 2 == 1]
    odd_graph: nx.Graph = nx.induced_subgraph(graph, odd_degree_vertices)
    matching: list[tuple[int, int]] = nx.min_weight_matching(odd_graph)
    eulerian_multigraph: nx.MultiGraph = nx.MultiGraph(mst)
    for edge in matching:
        weight: float = graph[edge[0]][edge[1]]["weight"]
        eulerian_multigraph.add_edge(edge[0], edge[1], weight=weight)
    cycle: list[int] = list(nx.dfs_preorder_nodes(eulerian_multigraph, 0))
    cycle.append(0)
    return calculate_cost(cycle, graph)
