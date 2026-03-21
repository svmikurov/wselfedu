"""Mathematical discipline exercise web repositories."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Dependency, Factory

from apps.core.storages.services.iabc import AbstractUserStorage
from apps.math.models import (
    CalculationCondition,
    StudentCalculationCondition,
)
from apps.math.repositories.exercise import (
    CalculationConditionsRepository,
    StudentCalculationConditionsRepository,
)
from apps.study.resolvers.completion import CompletionResolver


class ExerciseRepositoryContainer(DeclarativeContainer):
    """Mathematical discipline exercise web repositories."""

    # ===========================================
    # External dependencies
    # -------------------------------------------
    cache_storage: Dependency[  # fmt: off
        AbstractUserStorage[CalculationCondition],
    ] = Dependency()  # fmt: on

    # ===========================================
    # Repositories
    # -------------------------------------------
    calculation_conditions = Factory(
        CalculationConditionsRepository,
        store_prefix='calculation_condition',
        storage=cache_storage,
        manager=CalculationCondition.objects,
    )
    student_calculation_conditions = Factory(
        StudentCalculationConditionsRepository,
        store_prefix='student_calculation_condition',
        storage=cache_storage,
        manager=StudentCalculationCondition.objects,
        resolver=Factory(CompletionResolver),
    )
    mentor_calculation_conditions = Factory(
        CalculationConditionsRepository,
        store_prefix='mentor_calculation_condition',
        storage=cache_storage,
        manager=CalculationCondition.objects,
    )
