"""Implementa os algoritmos para solução do caixeiro viajante."""
import heapq
from math import inf

import networkx as nx

from src.algorithms.bounds import initial_bound, update_bound
from src.algorithms.node import Node
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
    eulerian_multigraph: nx.MultiGraph = nx.MultiGraph()
    eulerian_multigraph.add_edges_from(mst.edges)
    eulerian_multigraph.add_edges_from(matching)
    edges: list[tuple[int, int]] = list(nx.eulerian_circuit(eulerian_multigraph, 0))
    nodes: list[int] = [0]
    for _, v in edges:
        if v in nodes:
            continue
        nodes.append(v)
    nodes.append(0)
    return calculate_cost(nodes, graph)


def branch_and_bound(graph: nx.Graph) -> float:
    """Retorne o custo do TSP de `graph` usando o `branch_and_bound`."""
    n: int = graph.number_of_nodes()
    boundary, min_weights = initial_bound(graph)
    root: Node = Node(boundary, 1, 0, [0], min_weights)
    queue: list[Node] = [root]
    heapq.heapify(queue)
    best: float = inf
    while len(queue) != 0:
        node: Node = queue.pop(0)
        if node.level > n:
            if best > node.cost:
                best = node.cost
        elif node.boundary < best:
            if node.level < n:
                for k in range(1, n):
                    new_node = _branch_and_bound_helper(graph, k, node, best)
                    if new_node is not None:
                        heapq.heappush(queue, new_node)
            else:
                cycle_node = _branch_and_bound_helper(graph, 0, node, best)
                if cycle_node is not None:
                    heapq.heappush(queue, cycle_node)
    return best


def _branch_and_bound_helper(graph: nx.Graph, k: int, node: Node, best: float) -> Node:
    if (k not in node.sol or k == 0) and graph.has_edge(node.sol[-1], k):
        new_bound, new_min_weights = update_bound(graph, k, node)
        if new_bound < best:
            new_weight: float = graph[node.sol[-1]][k]["weight"]
            new_node: Node = Node(
                new_bound,
                node.level + 1,
                node.cost + new_weight,
                node.sol + [k],
                new_min_weights,
            )
            return new_node
    return None
