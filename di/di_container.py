"""Defines the Core dependency injection container."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Container

from apps.core.di.container import CoreContainer
from apps.glossary.di_container import GlossaryContainer
from apps.lang.di.container import LanguageContainer
from apps.math.di.container import MathematicalContainer
from apps.study.di_container import StudyAppContainer
from apps.users.di_container import UsersContainer


class MainContainer(DeclarativeContainer):
    """Main DI container."""

    core: Container[CoreContainer] = Container(
        CoreContainer,
    )
    users: Container[UsersContainer] = Container(
        UsersContainer,
    )
    study: Container[StudyAppContainer] = Container(
        StudyAppContainer,
    )

    # -------------------------------------------
    # Discipline containers
    # -------------------------------------------

    math: Container[MathematicalContainer] = Container(
        MathematicalContainer,
        task_storage=core.task_storage,
        award_service=users.award_service,
        study_container=study,
    )
    glossary: Container[GlossaryContainer] = Container(
        GlossaryContainer,
    )
    lang: Container[LanguageContainer] = Container(
        LanguageContainer,
        domains=core.domains,
        configuration=core.configuration,
    )
