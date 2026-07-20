"""Application layer protocols."""

from typing import Protocol, TypeVar

T_co = TypeVar('T_co', covariant=True)
T_contra = TypeVar('T_contra', contravariant=True)


class Executable(Protocol[T_contra, T_co]):
    def execute(self, cmd: T_contra) -> T_co: ...
