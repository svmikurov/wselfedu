"""Pytest configuration."""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable

import pytest

from wse.application.use_case import CheckAnswerUseCase, CreateTaskUseCase
from wse.domain.entities import ItemStudy
from wse.domain.services.task import CheckTestingService, CreateTestingService

from .fake.repository import FakeCandidatesRepository

if TYPE_CHECKING:
    from wse.domain.protocols import (
        CandidatesRepositoryProtocol,
        Testable,
        UniqueLearnable,
    )


def get_pk() -> Callable[[], int]:
    """Provide an unique database identifier."""
    counter = 0

    def _get_nex() -> int:
        nonlocal counter
        counter += 1
        return counter

    return _get_nex


CANDIDATES: list[UniqueLearnable] = [
    ItemStudy(get_pk(), 'definition-1', 'explanation-1'),  # type: ignore
    ItemStudy(get_pk(), 'definition-2', 'explanation-2'),  # type: ignore
    ItemStudy(get_pk(), 'definition-3', 'explanation-3'),  # type: ignore
    ItemStudy(get_pk(), 'definition-4', 'explanation-4'),  # type: ignore
    ItemStudy(get_pk(), 'definition-5', 'explanation-5'),  # type: ignore
]


@pytest.fixture
def candidates() -> list[UniqueLearnable]:
    """Provide a candidates for exercise."""
    return CANDIDATES


@pytest.fixture
def candidates_fake_repo(
    candidates: list[UniqueLearnable],
) -> CandidatesRepositoryProtocol:
    """Provide a task candidates fake (in-memory) repository."""
    return FakeCandidatesRepository(candidates)


###################################################
# Testing exercise fixtures
###################################################


@pytest.fixture
def create_testing_domain() -> CreateTestingService:
    """Provide a create testing task service."""
    return CreateTestingService()


@pytest.fixture
def check_testing_domain() -> CheckTestingService:
    """Provide a check testing answer service."""
    return CheckTestingService()


@pytest.fixture
def create_testing_task_use_case(
    candidates_fake_repo: CandidatesRepositoryProtocol,
    create_testing_domain: CreateTestingService,
) -> CreateTaskUseCase[Testable]:
    """Provide a create testing task  use case."""
    return CreateTaskUseCase(
        repository=candidates_fake_repo,
        domain=create_testing_domain,
    )


@pytest.fixture
def check_testing_answer_use_case(
    check_testing_domain: CheckTestingService,
) -> CheckAnswerUseCase:
    """Provide a create testing task  use case."""
    return CheckAnswerUseCase(domain=check_testing_domain)
