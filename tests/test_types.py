"""Types for tests."""

from typing import TypedDict


class LearnableTypedData(TypedDict):
    """Typed dict for learnable."""

    pk: int
    define: str
    explain: str
