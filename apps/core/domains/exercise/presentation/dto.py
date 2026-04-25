"""Core presentation DTOs."""

from typing import TypeVar

from interfaces.schemas.base import BaseDTO
from interfaces.schemas.domain.exercise.fields import OptionField
from interfaces.schemas.fields import ResourceIdentifierField

OptionT = TypeVar('OptionT')


class PresentationDomainResult(
    OptionField[OptionT],
):
    """Presentation exercise create domain result.

    Parameter
    ---------
    option : ...
        Exercise option field.

    """


# DEPRECATED:
class PresentationMeta(
    ResourceIdentifierField,
    BaseDTO,
):
    """Presentation exercise meta.

    Parameter
    ---------
    pk : `int`
        Stored presentation exercise database identifier.

    """
