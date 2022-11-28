"""Implementa um nó usado no Branch And Bound."""
from __future__ import annotations


class Node:
    """Representa um nó do Branch-and-Bound."""

    def __init__(
        self: Node,
        boundary: float,
        level: int,
        cost: float,
        sol: list[int],
    ) -> None:
        """Constrói um nó do Branch-and-Bound."""
        self.boundary = boundary
        self.level = level
        self.cost = cost
        self.sol = sol

    def __lt__(self: Node, other: Node) -> bool:
        """Compare duas Nodes usando o custo."""
        return self.cost < other.cost
