"""Programa principal."""

import pandas as pd

from src.util import generate_instances


def run() -> None:
    """Gere instâncias, rode os algoritmos e colete as métricas."""
    df: pd.DataFrame = generate_instances()
