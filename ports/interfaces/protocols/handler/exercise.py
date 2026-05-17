"""Protocols for exercise reqeust handler DTO inteface."""

from ports.interfaces.protocols.web import RequestDataProtocol
from ports.interfaces.request.web.exercise import (
    CheckTestData,
    CreateTaskData,
    UpdateProgressData,
)

# =================================================
# Exercise request data handler DTO interface
# =================================================

type CreateRequestDataT = RequestDataProtocol[CreateTaskData]
type CheckRequestDataT = RequestDataProtocol[CheckTestData]
type UpdateProgressRequestDataT = RequestDataProtocol[UpdateProgressData]
