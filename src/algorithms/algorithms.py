"""Implementa os algoritmos para solução do caixeiro viajante."""
import heapq
from math import ceil, inf

import networkx as nx

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
    boundary: float = bound(graph, [0])
    root: Node = Node(boundary, 1, 0, [0])
    queue: list[Node] = [root]
    heapq.heapify(queue)
    best: float = inf
    while len(queue) != 0:
        node: Node = queue.pop(0)
        if node.level > n:
            if best > node.cost:
                best = node.cost
        elif node.boundary < best:
            cycle_bound: float = bound(graph, node.sol + [0])
            if node.level < n:
                for k in range(1, n):
                    new_bound: float = bound(graph, node.sol + [k])
                    if (
                        k not in node.sol
                        and graph.has_edge(node.sol[-1], k)
                        and new_bound < best
                    ):
                        new_weight: float = graph[node.sol[-1]][k]["weight"]
                        new_node: Node = Node(
                            new_bound,
                            node.level + 1,
                            node.cost + new_weight,
                            node.sol + [k],
                        )
                        heapq.heappush(queue, new_node)
            elif graph.has_edge(node.sol[-1], 0) and cycle_bound < best:
                cycle_weight: float = graph[node.sol[-1]][0]["weight"]
                cycle_node: Node = Node(
                    cycle_bound, node.level + 1, node.cost + cycle_weight, node.sol + [0]
                )
                heapq.heappush(queue, cycle_node)
    return best


def bound(graph: nx.Graph, path: list[int]) -> float:
    """Estima, por baixo, qual seria o melhor caminho ainda possível."""
    size: int = graph.number_of_nodes()
    boundary: float = 0
    min_weights: list[tuple[float, float, bool]] = []
    for i in range(size):
        smallest: tuple[float, float] = (inf, inf, False)
        for j in range(size):
            if i == j:
                continue
            weight: float = graph[i][j]["weight"]
            if weight < smallest[0]:
                smallest = (weight, smallest[0], False)
            elif weight < smallest[1]:
                smallest = (smallest[0], weight, False)
        min_weights.append(smallest)
        boundary += smallest[0] + smallest[1]
    edges: list[tuple[int, int]] = []
    size: int = len(path)
    for i in range(0, size - 1):
        edges.append((path[i], path[i + 1]))
    increment: float = 0
    for edge in edges:
        u, v = edge
        if not graph.has_edge(u, v):
            continue
        weight = graph[u][v]["weight"]
        u_min = min_weights[u]
        if weight > u_min[0]:
            if not u_min[2]:
                increment += weight - u_min[1]
                min_weights[u] = (u_min[0], weight, True)
            else:
                increment += weight - u_min[0]

        v_min = min_weights[v]
        if weight > v_min[0]:
            if not v_min[2]:
                increment += weight - v_min[1]
                min_weights[v] = (v_min[0], weight, True)
            else:
                increment += weight - v_min[0]

    boundary += increment

    return ceil(boundary / 2)
