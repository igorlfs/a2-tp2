"""Testes para algumas propriedades dos geradores."""

import pytest

from src.generators import generate_points


def test_generate_points_exception() -> None:
    """Capture exceções de generate_points."""
    with pytest.raises(Exception, match="Muitos pontos para pouco espaço!"):
        generate_points(10, 1, 2)
