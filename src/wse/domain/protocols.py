"""Protocols for domain layer interface."""

from typing import Protocol, TypeVar

T = TypeVar('T')


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


class HasQuestionValue(Protocol):
    @property
    def question_value(self) -> int: ...


class HasQuestionText(Protocol):
    @property
    def question_text(self) -> str: ...


class HasOptionValue(Protocol):
    @property
    def option_value(self) -> int: ...


class HasOptionText(Protocol):
    @property
    def option_text(self) -> str: ...


class HasOptions(Protocol[T]):
    @property
    def options(self) -> list[T]: ...


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


class Selectable(
    HasOptionValue,
    HasOptionText,
    Protocol,
): ...


class Testable(
    HasQuestionText,
    HasQuestionValue,
    HasOptions[Selectable],
    Protocol,
): ...
