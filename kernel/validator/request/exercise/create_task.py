"""Validator for exercise action request data."""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from ports.abstract.validator import AbstractRequestValidator
from ports.contract.entity.domain.general import ActionTyped, HasAction
from ports.contract.enums.exercise import ExerciseAction
from ports.interfaces.protocols.web import RequestDataProtocol
from utils.audit.base import BaseAuditable

if TYPE_CHECKING:
    from utils.audit.protocol import AuditorProtocol

    type RegistryT = dict[
        ExerciseAction,
        Callable[..., HasAction[ExerciseAction]],
    ]

type DataT = RequestDataProtocol[ActionTyped[ExerciseAction]]
type ValidatedT = HasAction[ExerciseAction]


class ExerciseRequestValidator(
    BaseAuditable,
    AbstractRequestValidator[DataT, ValidatedT],
):
    """Validator for exercise action request data."""

    def __init__(
        self,
        schema_class_registry: RegistryT,
        name: str | None = None,
        auditor: AuditorProtocol | None = None,
    ) -> None:
        """Construct the validator."""
        super().__init__(name, auditor)
        self._schema_class_registry = schema_class_registry

    def validate(self, data: DataT) -> ValidatedT:
        """Validate the request data."""
        schema_cls = self._schema_class_registry[data.data['action']]
        return schema_cls(**data.data)
