"""Language application DI container."""

from dependency_injector import containers, providers
from dependency_injector.providers import Factory

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

    # Services
    # --------

    db_service = providers.Factory(
        WordStudyRepository,
    )
    task_service = providers.Factory(
        WordStudyService,
    )

    # Repositories
    # ------------

    translation_repo = providers.Factory(
        CreateEnglishTranslation,
    )

    params_repo = providers.Factory(
        WordStudyParamsRepository,
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
