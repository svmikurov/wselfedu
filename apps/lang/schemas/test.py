"""Translation study test exercise schemas."""

from typing import TypeAlias

from pydantic import BaseModel, ConfigDict

from apps.core.domains.exercise.schema.dto import StoryDomainResult

from ..models import EnglishTranslation


class Translation(BaseModel):
    """Translation."""

    orm_model: EnglishTranslation
    model_config = ConfigDict(arbitrary_types_allowed=True)


StoryTranslationResult: TypeAlias = StoryDomainResult[Translation]
