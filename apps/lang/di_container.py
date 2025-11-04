"""Language application DI container."""

from dependency_injector import containers, providers
from dependency_injector.providers import Factory

from apps.core.storage.clients import DjangoCache
from apps.lang import schemas

from . import repositories, services
from .presenters import (
    EnglishTranslationPresenter,
    WordStudyParamsPresenter,
    WordStudyPresenter,
)
from .presenters.abc import WordStudyParamsPresenterABC
from .repositories import (
    CreateEnglishTranslation,
    WordStudyParamsRepository,
    WordStudyRepository,
)
from .services.study import WordStudyService


class LanguageContainer(containers.DeclarativeContainer):
    """Language discipline DI container."""

    # Configurations
    # --------------

    progress_config = schemas.ProgressConfigSchema(
        increment=1,
        decrement=1,
    )

    # External dependencies
    # ----------------------

    django_cache: providers.Dependency[
        DjangoCache[schemas.WordStudyCaseSchema]
    ] = providers.Dependency()

    # Repositories
    # ------------

    translation_repo = providers.Factory(
        CreateEnglishTranslation,
    )

    params_repo = providers.Factory(
        WordStudyParamsRepository,
    )

    progress_repo = providers.Factory(
        repositories.UpdateWordProgressRepo,
    )

    # Services
    # --------

    db_service = providers.Factory(
        WordStudyRepository,
    )
    task_service = providers.Factory(
        WordStudyService,
    )

    progress_service = providers.Factory(
        services.UpdateWordProgressService,
        progress_repo=progress_repo,
        case_storage=django_cache,
        progress_config=progress_config,
    )

    # Presenters
    # ----------

    translation_presenter = providers.Factory(
        EnglishTranslationPresenter,
    )

    params_presenter: Factory[WordStudyParamsPresenterABC] = Factory(
        WordStudyParamsPresenter,
        repo=params_repo,
    )

    word_study_presenter = providers.Factory(
        WordStudyPresenter,
        db_service=db_service,
        task_service=task_service,
    )
