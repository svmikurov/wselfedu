"""Exercise handler types."""

from typing import Any

from apps.core.handlers import (
    RegularRequestHandler,
    ResourceRequestHandler,
)

# TEMPORARY: Using Any due to pending class definitions
# TODO: Replace with concrete types once classes are available
type RegularCalculationWebHandler = RegularRequestHandler[Any, Any, Any, Any]
type DetailCalculationWebHandler = ResourceRequestHandler[Any, Any, Any, Any]
type AssignedCalculationWebHandler = ResourceRequestHandler[Any, Any, Any, Any]


# EXPERIMENTAL:
# - Render calculation conditions as template data-attrs
type CalculationConditionsWebHandler = RegularRequestHandler[
    Any, Any, Any, Any
]
# - Calculation exercise performing
type CalculationExerciseWebHandler = RegularRequestHandler[Any, Any, Any, Any]
