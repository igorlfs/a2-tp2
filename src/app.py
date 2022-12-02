"""Programa principal."""

import networkx as nx
import pandas as pd

from src.generators import generate_instances, measure_algorithm


def run() -> pd.DataFrame:
    """Gere instâncias, rode os algoritmos e colete as métricas."""
    data: list[list] = []
    for i in range(4, 11):
        for metric in ("Euclidiana", "Manhattan"):
            instance: nx.Graph = generate_instances(i, metric)
            for algorithm in ("Twice Around The Tree", "Christofides"):
                execution: list = measure_algorithm(algorithm, instance, metric, i)
                data.append(execution)

    df: pd.DataFrame = pd.DataFrame(
        data, columns=["Instância", "Algoritmo", "Distância", "Tempo", "Custo"]
    )

    return df
