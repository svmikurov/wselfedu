"""Business interface."""

from typing import Protocol

# REVIEW: Type import
from apps.core.domains.exercise.enums import DisplayOrder

# =================================================
# Exercise parameters interface
# =================================================

# Conditions
# ----------


class HasCategory(Protocol):
    """Protocol for has *category* interface."""

    category: int | None


class HasMark(Protocol):
    """Protocol for has *mark* interface."""

    mark: list[int]


class HasSource(Protocol):
    """Protocol for has *source* interface."""

    source: int | None


class HasPeriod(Protocol):
    """Protocol for has *start_period*, *end_period* interface."""

    start_period: int | None
    end_period: int | None


class HasProgress(Protocol):
    """Protocol for has progress interface."""

    is_study: bool = True
    is_repeat: bool = True
    is_examine: bool = True
    is_know: bool = True


# Configuration
# -------------


class HasDisplayOrder(Protocol):
    """Protocol for item display order object interface."""

    display_order: DisplayOrder


class HasItemCount(Protocol):
    """Protocol for item count object interface."""

    item_count: int | None


class HasOptionCount(Protocol):
    """Protocol for item option count object interface."""

    option_count: int


# Settings
# --------


class HasTimeout(Protocol):
    """Protocol for exercise phase timeout interface."""

    question_timeout: int | None = None
    answer_timeout: int | None = None
