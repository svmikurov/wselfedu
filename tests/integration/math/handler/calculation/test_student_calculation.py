"""Student calculation perform handler tests.

Tests of start and check calculation exercise handlers.
"""

from typing import Any

import pytest
from wse_exercises.core.math import ExactOperandGenerator

from apps.core.adapters.response.exercise.generic import (
    ResultContextStrategyAdapter,
)
from apps.core.adapters.response.exercise.web.dto import WebExerciseResponseDTO
from apps.core.domains.exercise.enums import ExerciseStatusEnum
from apps.core.factories.abstract import AbstractExerciseDTOFactory
from apps.core.handlers.dto import DetailParams, RequestContext, RequestData
from apps.core.handlers.generic import ContextRequestHandler
from apps.core.handlers.protocol import (
    ContextResponseAdapterProtocol,
    DetailUseCaseProtocol,
    RequestValidatorProtocol,
    ResponseAdapterProtocol,
)
from apps.core.services.exercise.abstract import (
    AbstractExerciseCheck,
    AbstractExerciseExplain,
    AbstractRegularExerciseCreate,
)
from apps.core.storages.clients.django_cache import DjangoKeyCache
from apps.core.storages.services.iabc import AbstractUserStorage
from apps.core.storages.services.service import UserDataStorage
from apps.core.use_cases.abstract import (
    AbstractDetailDataUseCase,
    AbstractDetailUseCase,
)
from apps.core.validators.request.abstract import AbstractRequestValidator
from apps.core.validators.request.null import NullValidator
from apps.math.adapters.response.web.dto import ExerciseWebDTO
from apps.math.adapters.response.web.exercise import (
    CalculationWebCaseAdapter,
    ExplainCalculationWebAdapter,
    StudentCalculationWebCaseAdapter,
)
from apps.math.di.service.exercise import CALCULATION_DOMAIN_TYPES
from apps.math.domains.dto import (
    CalculationAnswerDTO,
    CalculationCaseDTO,
    CalculationConditionDTO,
    CalculationDomainDTO,
    CalculationExplainDTO,
    CalculationMetaDTO,
    CalculationResultDTO,
    ExerciseAvailabilityDTO,
    ExerciseCompletionDTO,
    ExerciseRewardDTO,
    StudentCalculationDTO,
    StudentParametersDTO,
)
from apps.math.domains.dto_factory import StudentCalculationDTOFactory
from apps.math.milestones.calculation import StudentCalculationMilestone
from apps.math.milestones.protocol import MilestoneServiceProtocol
from apps.math.models import StudentCalculationCondition
from apps.math.repositories.exercise import (
    BaseCalculationRepository,
    StudentCalculationConditionsRepository,
)
from apps.math.services.calculation import (
    CalculationCheckService,
    CalculationCreateService,
    CalculationExplainService,
)
from apps.math.use_cases.calculation import (
    DetailCalculationCheckUseCase,
    DetailExerciseCreateUseCase,
)
from apps.math.validators.web.exercise import (
    DetailCalculationCheckWebValidator,
)
from apps.study.resolvers.completion import CompletionResolver
from apps.study.services.abstract import AbstractCompletionService
from apps.study.services.completion import ExerciseCompletionService
from apps.users.models import Person
from apps.users.services.abstract import AbstractRewardService
from apps.users.services.reward import RewardService

# =================================================
# Validators
# =================================================


# Start and check exercise request have no data to validate.
@pytest.fixture
def create_validator() -> NullValidator[Any]:
    """Provide null validator."""
    return NullValidator()


@pytest.fixture
def check_validator() -> AbstractRequestValidator[CalculationAnswerDTO]:
    """Provide calculation exercise check validator."""
    return DetailCalculationCheckWebValidator()


# =================================================
# Storage & Repository
# =================================================


# Exercise data cache key contains user ID.
@pytest.fixture
def storage() -> AbstractUserStorage[Any]:
    """Provide data storage."""
    cache: DjangoKeyCache[Any] = DjangoKeyCache()
    return UserDataStorage(storage=cache)


@pytest.fixture
def repository(
    storage: UserDataStorage[Any],
) -> BaseCalculationRepository[StudentParametersDTO]:
    """Provide student calculation repository."""
    return StudentCalculationConditionsRepository(
        manager=StudentCalculationCondition.objects,
        storage=storage,
        resolver=CompletionResolver(),
    )


# =================================================
# Exercise services
# =================================================


@pytest.fixture
def create_service() -> CalculationCreateService:
    """Provide create calculation exercise service."""
    return CalculationCreateService(
        domains=CALCULATION_DOMAIN_TYPES,
        operand_generator=ExactOperandGenerator(),
    )


@pytest.fixture
def check_service() -> AbstractExerciseCheck[
    CalculationAnswerDTO,
    CalculationMetaDTO,
    CalculationResultDTO,
]:
    """Provide exercise check service."""
    return CalculationCheckService()


@pytest.fixture
def explain_service() -> AbstractExerciseExplain[
    CalculationAnswerDTO,
    CalculationMetaDTO,
    CalculationExplainDTO,
]:
    """Provide exercise calculation case service."""
    return CalculationExplainService()


# =================================================
# Adapters
# =================================================


@pytest.fixture
def create_adapter() -> ContextResponseAdapterProtocol[StudentCalculationDTO]:
    """Provide DTO factory."""
    domain_adapter = CalculationWebCaseAdapter()
    return StudentCalculationWebCaseAdapter(domain_adapter)


@pytest.fixture
def explain_adapter() -> ResponseAdapterProtocol[CalculationExplainDTO]:
    """Provide check exercise provider."""
    return ExplainCalculationWebAdapter()


# After user answer check the domain data adapted for
# new exercise case or explain correct answer response.
@pytest.fixture
def result_adapter_strategy(
    create_adapter: ContextResponseAdapterProtocol[CalculationExplainDTO],
    explain_adapter: ResponseAdapterProtocol[CalculationExplainDTO],
) -> ContextResponseAdapterProtocol[CalculationExplainDTO]:
    """Provide student calculation result strategy."""
    return ResultContextStrategyAdapter(
        new_case_adapter=create_adapter,
        explain_adapter=explain_adapter,
    )


# =================================================
# Milestone
# =================================================


@pytest.fixture
def completion_service() -> AbstractCompletionService[
    StudentCalculationCondition
]:
    """Provide completion service."""
    return ExerciseCompletionService(
        manager=StudentCalculationCondition.objects
    )


@pytest.fixture
def reward_service() -> AbstractRewardService:
    """Provide milestone service."""
    return RewardService()


@pytest.fixture
def milestone_service(
    reward_service: AbstractRewardService,
    completion_service: AbstractCompletionService[StudentCalculationCondition],
) -> MilestoneServiceProtocol[
    CalculationMetaDTO,
    CalculationResultDTO,
    ExerciseAvailabilityDTO,
    ExerciseCompletionDTO,
    ExerciseRewardDTO,
]:
    """Provide milestone service."""
    return StudentCalculationMilestone(
        reward_service=reward_service,
        completion_service=completion_service,
        exercise_manager=StudentCalculationCondition.objects,
    )


# =================================================
# Use cases
# =================================================


# Factory to create DTO for response adapter
@pytest.fixture
def dto_factory() -> AbstractExerciseDTOFactory[
    CalculationDomainDTO,
    StudentParametersDTO,
    StudentCalculationDTO,
]:
    """Provide DTO factory."""
    return StudentCalculationDTOFactory()


@pytest.fixture
def create_use_case(
    repository: StudentCalculationConditionsRepository,
    create_service: AbstractRegularExerciseCreate[
        CalculationConditionDTO,
        tuple[CalculationCaseDTO, CalculationMetaDTO],
    ],
    storage: UserDataStorage[Any],
    dto_factory: AbstractExerciseDTOFactory[
        CalculationCaseDTO,
        StudentParametersDTO,
        StudentCalculationDTO,
    ],
) -> AbstractDetailUseCase[StudentCalculationDTO]:
    """Provide calculation exercise use case."""
    return DetailExerciseCreateUseCase(
        repository=repository,
        service=create_service,
        storage=storage,
        dto_factory=dto_factory,
    )


@pytest.fixture
def check_use_case(
    storage: UserDataStorage[Any],
    repository: StudentCalculationConditionsRepository,
    check_service: AbstractExerciseCheck[
        CalculationAnswerDTO,
        CalculationCaseDTO,
        CalculationResultDTO,
    ],
    explain_service: AbstractExerciseExplain[
        CalculationAnswerDTO,
        CalculationCaseDTO,
        CalculationExplainDTO,
    ],
    milestone_service: MilestoneServiceProtocol[
        CalculationMetaDTO,
        CalculationResultDTO,
        ExerciseAvailabilityDTO,
        ExerciseCompletionDTO,
        ExerciseRewardDTO,
    ],
    create_use_case: AbstractDetailUseCase[CalculationCaseDTO],
) -> AbstractDetailDataUseCase[
    CalculationAnswerDTO,
    CalculationCaseDTO | CalculationExplainDTO,
]:
    """Provide calculation exercise use case."""
    return DetailCalculationCheckUseCase(
        storage=storage,
        check_service=check_service,
        repository=repository,
        milestone_service=milestone_service,
        create_use_case=create_use_case,
        explain_service=explain_service,
    )


# =================================================
# Handlers
# =================================================


@pytest.fixture
def start_handler(
    create_validator: NullValidator[Any],
    create_use_case: DetailUseCaseProtocol[Any, Any],
    create_adapter: ContextResponseAdapterProtocol[Any],
) -> ContextRequestHandler[Any, Any]:
    """Provide student calculation start handler."""
    return ContextRequestHandler(
        validator=create_validator,
        use_case=create_use_case,
        adapter=create_adapter,
    )


@pytest.fixture
def check_handler(
    check_validator: RequestValidatorProtocol[Any],
    check_use_case: DetailUseCaseProtocol[Any, Any],
    result_adapter_strategy: ContextResponseAdapterProtocol[Any],
) -> ContextRequestHandler[Any, Any]:
    """Provide student calculation check handler."""
    return ContextRequestHandler(
        validator=check_validator,
        use_case=check_use_case,
        adapter=result_adapter_strategy,
    )


# =================================================
# Tests
# =================================================


@pytest.mark.django_db
class TestStartStudentCalculationPerformHandler:
    """Start student calculation perform test."""

    def test_start_success(
        self,
        student: Person,
        start_handler: ContextRequestHandler[Any, Any],
        calculation_assignation: StudentCalculationCondition,
    ) -> None:
        """Start calculation perform success test."""
        # Act
        result_dto = start_handler.execute(
            params=DetailParams(pk=calculation_assignation.pk),
            context=RequestContext(user=student),
            data=RequestData(query={}),
        )

        # Assert
        # - Result DTO is `WebExerciseResponseDTO` type
        assert isinstance(result_dto, WebExerciseResponseDTO)

        # - Result DTO contains exercise status and status is new case
        assert result_dto.exercise_status is ExerciseStatusEnum.NEW_CASE

        # The text of the exercise question and context of the exercise
        # are defined using the `calculation_assignation` fixture.

        # - Result DTO data contains question text
        assert result_dto.data.question_text == '2 + 3'  # type: ignore[attr-defined]

        # - Result DTO contains exercise details context
        assert result_dto.context == {
            'exercise': {
                'success_count': 0,
                'required_count': 10,
            },
        }


@pytest.mark.django_db
class TestCheckStudentCalculationPerformHandler:
    """Student calculation check test."""

    @pytest.fixture(autouse=True)
    def setup(
        self,
        student: Person,
        start_handler: ContextRequestHandler[Any, Any],
        calculation_assignation: StudentCalculationCondition,
    ) -> None:
        """Create student calculation exercise."""
        start_handler.execute(
            params=DetailParams(pk=calculation_assignation.pk),
            context=RequestContext(user=student),
            data=RequestData(query={}),
        )

    def test_check_correct_answer(
        self,
        student: Person,
        check_handler: ContextRequestHandler[Any, Any],
        calculation_assignation: StudentCalculationCondition,
    ) -> None:
        """Check calculation perform success test."""
        # Act
        result_dto = check_handler.execute(
            params=DetailParams(pk=calculation_assignation.pk),
            context=RequestContext(user=student),
            data=RequestData(
                query={
                    # Correct answer
                    'user_answer': '5',
                }
            ),
        )

        # Assert
        # - Result DTO is `WebExerciseResponseDTO` type
        assert isinstance(result_dto, WebExerciseResponseDTO)

        # - Result DTO contains exercise status and status is new case
        assert result_dto.exercise_status is ExerciseStatusEnum.NEW_CASE

        # The text of the exercise question and context of the exercise
        # are defined using the `calculation_assignation` fixture.

        # - Result DTO data contains question text
        assert result_dto.data.question_text == '2 + 2'  # type: ignore[attr-defined]

        # - Result DTO contains exercise details context
        assert result_dto.context == {
            'exercise': {
                # FIXME: Increase success count
                'success_count': 0,
                'required_count': 10,
            },
        }

    def test_check_wrong_answer(
        self,
        student: Person,
        check_handler: ContextRequestHandler[Any, Any],
        calculation_assignation: StudentCalculationCondition,
    ) -> None:
        """Check calculation perform success test."""
        # Act
        result_dto = check_handler.execute(
            params=DetailParams(pk=calculation_assignation.pk),
            context=RequestContext(user=student),
            data=RequestData(
                query={
                    # Wrong answer
                    'user_answer': '4',
                }
            ),
        )

        # Assert
        # - Result DTO is `ExerciseWebDTO` type
        # REVIEW: Replace result DTO?
        assert isinstance(result_dto, ExerciseWebDTO)

        # - Result DTO contains exercise status and status is "Explain"
        assert result_dto.exercise_status is ExerciseStatusEnum.EXPLAIN

        # - Result DTO data contains explain text
        assert not hasattr(result_dto.data, 'question_text')
        assert result_dto.data.solution_text == '2 + 3 = 5'  # type: ignore[attr-defined]

        # - Result DTO have no exercise details context
        assert result_dto.context == {}
