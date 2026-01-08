"""Test exercise services."""

from __future__ import annotations

import random
import uuid
from typing import TYPE_CHECKING, Any

from django.db.models import QuerySet

from apps.core.storage.services import TaskStorage

from ..models import EnglishTranslation
from ..schemas.test import (
    Case,
    CaseStatus,
    Explanation,
    Option,
    OptionId,
    StoryDomainResult,
    Translation,
)

if TYPE_CHECKING:
    from django.db.models import QuerySet

    from apps.users.models import Person

    from ..repositories import ProgressABC, TranslationRepoABC
    from ..schemas import TestRequestDTO

    type Storage = TaskStorage[StoryDomainResult]
    type CaseCandidates = QuerySet[EnglishTranslation]
    type Config = dict[str, Any]

    # UseCase generic types
    type RequestDTO = TestRequestDTO
    type DomainResult = Case | Explanation

# TODO: Refactor
# - SOLID


class TestService:
    """Test exercise services."""

    def __init__(
        self,
        repository: TranslationRepoABC,
        storage: TaskStorage[StoryDomainResult],
        config: Config,
        domain: None = None,
    ) -> None:
        """Construct the service."""
        self._repository = repository
        self._domain = domain
        self._storage = storage
        self._config = config

    def execute(self, user: Person, request: RequestDTO) -> DomainResult:
        """Create test case, check user answer."""
        match request.status:
            case CaseStatus.NEW:
                return self._create_case(user)

            case CaseStatus.ANSWER:
                return self._check_case(user, request)

            case _:
                raise ValueError(f'Unexpected test status: {request.status}')

    def _create_case(self, user: Person) -> DomainResult:
        question_option = random.randrange(self._config['option_count'])

        translations = self._get_translations(user)
        translation = translations[question_option]
        question = translation.foreign.word
        answer = translation.native.word

        option_ids: list[OptionId] = []
        options: list[Option] = []
        for value, option in enumerate(translations):
            option_ids.append(OptionId(value=value, id=option.pk))
            options.append(Option(value=value, text=option.native.word))

        to_story = StoryDomainResult(
            translations=tuple(Translation(orm_model=t) for t in translations),
            question=question,
            answer=answer,
            id=translation.pk,
            option_value=question_option,
            option_ids=option_ids,
        )
        case_uuid = self._storage.save_task(to_story)

        return Case(
            case_uuid=str(case_uuid),
            question=question,
            options=options,
        )

    def _check_case(self, user: Person, request: RequestDTO) -> DomainResult:
        if request.option_value is None:
            raise ValueError('Expected option value')
        if request.case_uuid is None:
            raise ValueError('Expected test case uuid')

        answer_option_value = int(request.option_value)

        from_story = self._storage.retrieve_task(uuid.UUID(request.case_uuid))

        if from_story.option_value == answer_option_value:
            return self._create_case(user)

        selected_translation = from_story.translations[
            answer_option_value
        ].orm_model

        return Explanation(
            case_question=from_story.question,
            case_answer=from_story.answer,
            selected_question=selected_translation.native.word,
            selected_answer=selected_translation.foreign.word,
        )

    # TODO: Exclude word translation duplicates.
    # Native and foreign words may have any translations.
    def _get_translations(self, user: Person) -> list[EnglishTranslation]:
        limit = self._config['limit']
        option_count = self._config['option_count']

        latest_translations = EnglishTranslation.objects.filter(
            user=user
        ).order_by('-created_at')[:limit]

        if len(latest_translations) >= option_count:
            case_translations = random.sample(
                tuple(latest_translations), option_count
            )
        else:
            raise ValueError('Not enough translations')

        return case_translations


class TestProgressService:
    """Test exercise services with progress tracking."""

    INCREMENT_PROGRESS_DELTA = 1
    DECREMENT_PROGRESS_DELTA = -1

    def __init__(
        self,
        repository: TranslationRepoABC,
        progress_repository: ProgressABC,
        storage: Storage,
        config: Config,
        domain: None = None,
    ) -> None:
        """Construct the service."""
        self._repository = repository
        self._progress_repository = progress_repository
        self._domain = domain
        self._storage = storage
        self._config = config

    def execute(self, user: Person, request: RequestDTO) -> DomainResult:
        """Create test case, check user answer."""
        match request.status:
            case CaseStatus.NEW:
                return self._create_case(user)

            case CaseStatus.ANSWER:
                return self._check_case(user, request)

            case _:
                raise ValueError(f'Unexpected test status: {request.status}')

    def _create_case(self, user: Person) -> DomainResult:
        question_option = random.randrange(self._config['option_count'])

        translations = self._get_translations(user)
        translation = translations[question_option]
        question = translation.foreign.word
        answer = translation.native.word

        option_ids: list[OptionId] = []
        options: list[Option] = []
        for value, option in enumerate(translations):
            option_ids.append(OptionId(value=value, id=option.pk))
            options.append(Option(value=value, text=option.native.word))

        to_story = StoryDomainResult(
            translations=tuple(Translation(orm_model=t) for t in translations),
            question=question,
            answer=answer,
            id=translation.pk,
            option_value=question_option,
            option_ids=option_ids,
        )
        case_uuid = self._storage.save_task(to_story)

        return Case(
            case_uuid=str(case_uuid),
            question=question,
            options=options,
        )

    def _check_case(self, user: Person, request: RequestDTO) -> DomainResult:
        if request.option_value is None:
            raise ValueError('Expected option value')
        if request.case_uuid is None:
            raise ValueError('Expected test case uuid')

        answer_option_value = int(request.option_value)

        from_story = self._storage.retrieve_task(uuid.UUID(request.case_uuid))

        # User correct answer
        # -------------------

        if from_story.option_value == answer_option_value:
            # If user answer is correct then
            # incremented question translation study progress
            self._progress_repository.update(
                user=user,
                translation_id=from_story.id,
                progress_delta=self.INCREMENT_PROGRESS_DELTA,
            )
            return self._create_case(user)

        # User wrong answer
        # -----------------

        selected_translation = from_story.translations[
            answer_option_value
        ].orm_model

        # If user answer is wrong then
        # decremented question translation study progress and
        # decremented user answer translation study progress
        self._progress_repository.update(
            user=user,
            translation_id=from_story.id,
            progress_delta=self.DECREMENT_PROGRESS_DELTA,
        )
        self._progress_repository.update(
            user=user,
            translation_id=selected_translation.id,
            progress_delta=self.DECREMENT_PROGRESS_DELTA,
        )

        return Explanation(
            case_question=from_story.question,
            case_answer=from_story.answer,
            selected_question=selected_translation.native.word,
            selected_answer=selected_translation.foreign.word,
        )

    # TODO: Exclude word translation duplicates.
    # Native and foreign words may have any translations.
    def _get_translations(self, user: Person) -> list[EnglishTranslation]:
        limit = self._config['limit']
        option_count = self._config['option_count']

        latest_translations = EnglishTranslation.objects.filter(
            user=user
        ).order_by('-created_at')[:limit]

        if len(latest_translations) >= option_count:
            case_translations = random.sample(
                tuple(latest_translations), option_count
            )
        else:
            raise ValueError('Not enough translations')

        return case_translations
