"""Protocol for exercise request handler command interface."""

from typing import Protocol

from contracts.entity.general import HasData, HasUser
from interfaces.protocols.validated.exercise import (
    ValidatedCheckTestRequestProtocol,
    ValidatedCreateTaskRequestProtocol,
)


class CreateTaskCommandProtocol(
    HasUser,
    HasData[ValidatedCreateTaskRequestProtocol],
    Protocol,
):
    """protocol for create task command."""


class CheckTestCommandProtocol(
    HasUser,
    HasData[ValidatedCheckTestRequestProtocol],
    Protocol,
):
    """protocol for create task command."""
