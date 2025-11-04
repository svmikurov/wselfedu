"""Defines the Core dependency injection container."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Container

from apps.core.di_container import CoreContainer
from apps.glossary.di_container import GlossaryContainer
from apps.lang.di_container import LanguageContainer
from apps.math.di_container import MathAppContainer
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
    math: Container[MathAppContainer] = Container(
        MathAppContainer,
        task_storage=core.task_storage,
        award_service=users.award_service,
    )
    glossary: Container[GlossaryContainer] = Container(
        GlossaryContainer,
    )
    lang: Container[LanguageContainer] = Container(
        LanguageContainer,
        django_cache=core.django_cache,
    )
    study: Container[StudyAppContainer] = Container(
        StudyAppContainer,
    )
