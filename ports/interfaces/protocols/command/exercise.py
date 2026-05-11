"""Protocol for exercise request handler command interface."""

from typing import Protocol

from ports.contract.entity.general import HasData, HasUser
from ports.interfaces.protocols.validated.exercise import (
    ValidatedCheckTestRequestProtocol,
    ValidatedCreateTaskRequestProtocol,
)


class CreateTaskCommandProtocol(
    HasUser,
    HasData[ValidatedCreateTaskRequestProtocol],
    Protocol,
):
    """Protocol for create task command.

    Parameters
    ----------
    user : `Person`
        The user who performs the exercise.
    data : `ValidatedCreateTaskRequestProtocol`
        Create task validated data.

    """


class CheckTestCommandProtocol(
    HasUser,
    HasData[ValidatedCheckTestRequestProtocol],
    Protocol,
):
    """Protocol for check task answer command.

    Parameters
    ----------
    user : `Person`
        The user who performs the exercise.
    data : `ValidatedCheckTestRequestProtocol`
        User answer validated data.

    """
