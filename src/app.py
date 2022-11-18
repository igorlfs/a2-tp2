"""Programa principal."""
import networkx as nx
import numpy as np

import src.globals as g
from src.util import calculate_distance, generator


def run() -> None:
    """Gere instâncias, rode os algoritmos e colete as métricas."""
    # 1. Gerar um conjunto de pontos
    my_points: np.array = generator(5)

    # 2. Calcular as distâncias entre os pontos
    my_matrix: np.array = calculate_distance(my_points, g.EUCLIDIAN)

    # # 3. Construir um grafo que tem como vértices os pontos
    # # e como arestas (com peso) as distâncias
    my_graph = nx.from_numpy_matrix(my_matrix)
    nx.draw(my_graph)

    # 4. Rodar algum dos algoritmos no grafo
    # 4.1 Retornar tempo, espaço, qualidade da solução
