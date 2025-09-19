"""Glossary app DI container."""

from dependency_injector import containers, providers

from apps.glossary.presenters import TermStudyPresenter


class GlossaryContainer(containers.DeclarativeContainer):
    """Glossary discipline DI container."""

    term_study_presenter = providers.Factory(
        TermStudyPresenter,
    )
