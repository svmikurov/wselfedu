"""Domain layer contracts."""

from typing import Protocol

# #################################################
# Components
# #################################################


class HasIdentifier(Protocol):
    @property
    def pk(self) -> int: ...


class HasDefine(Protocol):
    @property
    def define(self) -> str: ...


class HasExplain(Protocol):
    @property
    def explain(self) -> str: ...


# #################################################
# Compositions
# #################################################


class Learnable(
    HasDefine,
    HasExplain,
    Protocol,
): ...


class UniqueLearnable(
    HasIdentifier,
    Learnable,
    Protocol,
): ...


###################################################
# Services
###################################################


class CreateTaskServiceProtocol(Protocol):
    def execute(self, candidates: list[Learnable]) -> Learnable: ...


###################################################
# Repositories
###################################################


class CandidatesRepositoryProtocol(Protocol):
    def list(self) -> list[Learnable]: ...
