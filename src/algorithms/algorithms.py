"""Implementa os algoritmos para solução do caixeiro viajante."""
import heapq
from math import ceil, inf

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


class Node:
    """Representa um nó do Branch-and-Bound."""

    def __init__(
        self,
        boundary: float,
        cost: float,
        level: int,
        sol: list[int],
        min_weights: list[tuple[float, float, bool]],
    ) -> None:
        self.boundary = boundary
        self.cost = cost
        self.level = level
        self.sol = sol
        self.min_weights = min_weights

    def __lt__(self, other) -> bool:
        return self.cost < other.level


def branch_and_bound(graph: nx.Graph) -> float:
    """Resolva o caixeiro viajanta para `graph` usando o `branch_and_bound`."""
    n: int = graph.number_of_nodes()
    min_weights: list[tuple[float, float, bool]] = []
    boundary = bound(graph, min_weights)
    root: Node = Node(boundary, 0, 0, [0], min_weights)
    queue: list[Node] = [root]
    heapq.heapify(queue)
    best = inf
    sol = []
    while len(queue) != 0:
        node: Node = queue.pop()
        if node.level >= n:
            if best > node.cost:
                best = node.cost
                sol = node.sol
        elif node.boundary < best:
            if node.sol[-1] != 0:
                loop_weight = graph[node.sol[-1]][0]["weight"]
                loop_edge = (node.sol[-1], 0, loop_weight)
                loop_weights, loop_bound = updateBound(
                    loop_edge, node.min_weights, node.boundary
                )
            else:
                loop_bound = inf
            if node.level < n:
                for k in range(1, n):
                    weight = graph[node.sol[-1]][k]["weight"]
                    edge = (node.sol[-1], k, weight)
                    new_weights, new_bound = updateBound(
                        edge, node.min_weights, node.boundary
                    )
                    if (
                        k not in node.sol
                        and graph[node.sol[-1]][k] != inf
                        and new_bound < best
                    ):
                        new_sol = node.sol.copy().append(k)
                        new_node: Node = Node(
                            new_bound,
                            node.level + 1,
                            node.cost + weight,
                            new_sol,
                            new_weights,
                        )
                        heapq.heappush(queue, new_node)
            elif (
                graph[node.sol[-1]][0] != inf and loop_bound < best
            ):  # and para todo i em node.sol
                loop_sol = node.sol.copy().append(0)
                new_node: Node = Node(
                    loop_bound,
                    node.level + 1,
                    node.cost + loop_weight,
                    loop_sol,
                    loop_weights,
                )
                heapq.heappush(queue, new_node)


def bound(graph: nx.Graph, min_weights: list[tuple[float, float, bool]]) -> float:
    """Estima, por baixo, qual seria o melhor caminho ainda possível."""
    size: int = graph.number_of_nodes()
    boundary: float = 0
    for i in range(size):
        smallest: tuple[float, float, bool] = (inf, inf, False)
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
    return ceil(boundary / 2)


def updateBound(
    edge: tuple[int, int, float],
    min_weights: list[tuple[float, float, bool]],
    boundary: float,
):
    min_weights_copy = min_weights.copy()
    boundary_copy = boundary

    increment: float = 0

    u, v, weight = edge

    u_min_weights: tuple[float, float, bool] = min_weights_copy[u]
    if not u_min_weights[2]:
        min_weights_copy[u] = (u_min_weights[0], u_min_weights[1], True)
        increment += weight - u_min_weights[1]
    else:
        increment += weight - u_min_weights[0]

    v_min_weights: tuple[float, float, bool] = min_weights_copy[v]
    if not v_min_weights[2]:
        min_weights_copy[v] = (v_min_weights[0], v_min_weights[1], True)
        increment += weight - v_min_weights[1]
    else:
        increment += weight - v_min_weights[0]

    boundary_copy += ceil(increment / 2)

    return min_weights_copy, boundary_copy
