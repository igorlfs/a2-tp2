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
    eulerian_multigraph.add_edges_from(matching)
    edges: list[tuple[int, int]] = list(nx.eulerian_circuit(eulerian_multigraph, 0))
    nodes: list[int] = [0]
    for _, v in edges:
        if v in nodes:
            continue
        nodes.append(v)
    nodes.append(0)
    return calculate_cost(nodes, graph)
