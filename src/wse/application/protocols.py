"""Application layer protocols."""

from typing import Protocol, TypeVar

T_cov = TypeVar('T_cov', covariant=True)
T_contra = TypeVar('T_contra', contravariant=True)


class HasTask(Protocol[T_cov]):
    @property
    def task(self) -> T_cov: ...


###################################################
# Commands
###################################################


class CerateTestingCommandProto(Protocol): ...


###################################################
# DTOs
###################################################


class TaskProto(
    HasTask[T_cov],
    Protocol[T_cov],
): ...


###################################################
# Use cases
###################################################


class Executable(Protocol[T_contra, T_cov]):
    def execute(self, cmd: T_contra) -> T_cov: ...
