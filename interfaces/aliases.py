"""Type aliases for common generic."""

from typing import TypeAlias

from .protocols.domain.exercise import Candidate, Candidates

CandidatesAlias: TypeAlias = Candidates[Candidate]
