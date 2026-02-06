"""Language service types."""

from __future__ import annotations

import uuid
from typing import TYPE_CHECKING, Any

from pydantic import BaseModel, Field

from apps.lang.schemas import RegularConditionRequest

# HACK: Replace Any
if TYPE_CHECKING:
    from apps.core.storage.services import TaskStorage
    from apps.lang import schemas
    from apps.lang.schemas import dto

    # Exercise case request
    type AssignedRequest = Any
    type RegularRequest = schemas.RegularConditionRequest

    # Exercise case
    type TestCase = StoredTestCaseDTO
    type PresentationCase = dto.PresentationCase

    # Exercise case storage
    type CaseStorage = TaskStorage[Any]


# HACK: Relocate schema definition
class TestAnswerDTO(BaseModel):
    """Test answer DTO."""


class CreateTestRequestDTO(BaseModel):
    """Request data DTO to create exercise case."""


class CheckTestRequestDTO(BaseModel):
    """Request data DTO to check exercise case."""

    case_uid: uuid.UUID = Field(description='Stored case UUID')
    answer: TestAnswerDTO
    condition: RegularConditionRequest


class TestCaseDTO(BaseModel):
    """New test exercise DTO."""


class CaseMetaDTO(BaseModel):
    """Exercise case meta data."""


class StoredTestCaseDTO(BaseModel):
    """New test exercise DTO."""

    uid: uuid.UUID
    case: TestCaseDTO


class TestExplanationDTO(BaseModel):
    """Exercise case explanation DTO."""


class CheckTestResultDTO(BaseModel):
    """Check user answer result on task exercise."""

    is_correct: bool
    explanation: TestExplanationDTO
