"""Translation repository types."""

from __future__ import annotations

from apps.lang import models, schemas

type Parameters = schemas.LookupCondition
type Translation = models.EnglishTranslation
