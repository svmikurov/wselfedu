"""Defines Study app DI container."""

from dependency_injector import containers, providers

from apps.study.selectors.assigned import AssignedSelector
from apps.study.servises.checker import StrTaskChecker


class StudyAppContainer(containers.DeclarativeContainer):
    """DI container for Study app dependencies."""

    assigned_exercises_selector = providers.Factory(
        AssignedSelector,
    )
    str_task_checker = providers.Factory(
        StrTaskChecker,
    )
