"""Word study presenter."""

import logging
from typing import override

from apps.users.models import CustomUser

from ..orchestrators.abc import WordStudyOrchestratorABC
from ..services.abc import WordStudyServiceABC
from ..types import WordParamsType, WordType
from .abc import WordStudyPresenterABC

log = logging.getLogger(__name__)


class WordStudyPresenter(WordStudyPresenterABC):
    """Presenter for Word study exercise."""

    def __init__(
        self,
        db_service: WordStudyOrchestratorABC,
        task_service: WordStudyServiceABC,
    ) -> None:
        """Construct the presenter."""
        self._db = db_service
        self._task_service = task_service

    @override
    def get_presentation(
        self,
        params: WordParamsType,
        user: CustomUser,
    ) -> WordType:
        """Get Word study presentation case."""
        candidates = self._db.get_candidates(params)

        # TODO: Add custom exception?
        if not candidates.ids:
            log.info('No words to study for request params')
            raise LookupError

        case_id = self._task_service.create(candidates)
        case = self._db.get_case(case_id.definition_id, user)
        return case
