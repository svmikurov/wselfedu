"""Language application DI container."""

from dependency_injector import containers, providers
from dependency_injector.providers import Factory

from .orchestrators import (
    CreateEnglishTranslation,
    WordStudyOrchestrator,
    WordStudyParamsOrchestrator,
)
from .presenters import (
    EnglishTranslationPresenter,
    WordStudyParamsPresenter,
    WordStudyPresenter,
)
from .presenters.abc import WordStudyParamsPresenterABC
from .services.study import WordStudyService


class LanguageContainer(containers.DeclarativeContainer):
    """Language discipline DI container."""

    # Services
    # --------

    db_service = providers.Factory(
        WordStudyOrchestrator,
    )
    task_service = providers.Factory(
        WordStudyService,
    )

    # Orchestrators
    # -------------

    translation_orchestrator = providers.Factory(
        CreateEnglishTranslation,
    )

    params_orchestrator = providers.Factory(
        WordStudyParamsOrchestrator,
    )

    # Presenters
    # ----------

    translation_presenter = providers.Factory(
        EnglishTranslationPresenter,
    )

    params_presenter: Factory[WordStudyParamsPresenterABC] = Factory(
        WordStudyParamsPresenter,
        orchestrator=params_orchestrator,
    )

    word_study_presenter = providers.Factory(
        WordStudyPresenter,
        db_service=db_service,
        task_service=task_service,
    )
