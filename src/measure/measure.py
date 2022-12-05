"""Colete algumas métricas, em particular da execução do algoritmo."""
import time

import networkx as nx

from src.algorithms import tsp_solver


def measure_algorithm(algorithm: str, graph: nx.Graph, metric: str, i: int) -> list:
    """Executa um algoritmo em uma instância e retorna suas métricas."""
    start: float = time.time()
    cost: float = tsp_solver(algorithm, graph)
    end: float = time.time()
    diff_time: float = end - start
    return [i, algorithm, metric, diff_time, cost]
