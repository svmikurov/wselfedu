"""Glossary app DI container."""

from dependency_injector import containers, providers

from apps.glossary.presenters import TermsStudyPresenter


class GlossaryContainer(containers.DeclarativeContainer):
    """Glossary discipline DI container."""

    terms_study_presenter = providers.Factory(
        TermsStudyPresenter,
    )
