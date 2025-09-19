"""Defines the Core dependency injection container."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Container

from apps.core.di_container import CoreContainer
from apps.glossary.di_container import GlossaryContainer
from apps.math.di_container import MathAppContainer
from apps.study.di_container import StudyAppContainer
from apps.users.di_container import UsersContainer


class MainContainer(DeclarativeContainer):
    """Main DI container."""

    core_container: Container[CoreContainer] = Container(
        CoreContainer,
    )
    users_container: Container[UsersContainer] = Container(
        UsersContainer,
    )
    math_container: Container[MathAppContainer] = Container(
        MathAppContainer,
        task_storage=core_container.task_storage,
        award_service=users_container.award_service,
    )
    glossary_container: Container[GlossaryContainer] = Container(
        GlossaryContainer,
    )
    study_container: Container[StudyAppContainer] = Container(
        StudyAppContainer,
    )
