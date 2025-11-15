"""Language application DI container."""

from dependency_injector import containers, providers
from dependency_injector.providers import Factory

from apps.core.storage.clients import DjangoCache
from apps.lang import schemas

from . import presenters, repos, services
from .presenters.abc import WordStudyParamsPresenterABC
from .services.presentation import WordPresentationService
from .services.study import WordStudyDomain


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

    params_repo = providers.Factory(
        repos.WordStudyParamsRepository,
    )
    word_repo = providers.Factory(
        repos.Presentation,
    )
    translation_repo = providers.Factory(
        repos.TranslationRepo,
    )
    progress_repo = providers.Factory(
        repos.UpdateWordProgressRepo,
    )

    # Domain
    # ------

    word_study_domain = providers.Factory(
        WordStudyDomain,
    )

    # Services
    # --------

    word_presentation_service = providers.Factory(
        WordPresentationService,
        word_repo=word_repo,
        translation_repo=translation_repo,
        case_storage=django_cache,
        domain=word_study_domain,
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
        presenters.EnglishTranslationPresenter,
    )

    params_presenter: Factory[WordStudyParamsPresenterABC] = Factory(
        presenters.WordStudyParamsPresenter,
        repo=params_repo,
    )
