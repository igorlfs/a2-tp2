"""Testes as exceções dos geradores."""

import pytest

from src.generate import generate_points


def test_generate_points_exception() -> None:
    """Capture exceções de generate_points."""
    with pytest.raises(Exception, match="Muitos pontos para pouco espaço!"):
        generate_points(10, 1, 2)
