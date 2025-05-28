"""Custom exceptions for the Math Exercises service.

This module defines a hierarchy of exceptions specific
to exercise processing, all following REST API exception
patterns from Django REST Framework.
"""

from rest_framework import status
from rest_framework.exceptions import APIException


class ExerciseConditionsException(APIException):
    """Raised when requested exercise with invalid conditions."""

    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Invalid exercise conditions'
    default_code = 'invalid_exercise_conditions'


class ExerciseServiceException(APIException):
    """Base exception for exercise-related errors.

    :param int status_code: HTTP status code (default: 500).
    :param str default_detail: Human-readable error description.
    :param str default_code: Machine-readable error code.
    """

    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = 'Exercise service error'
    default_code = 'exercise_service_error'


class ExerciseNotFound(ExerciseServiceException):
    """Raised when requested exercise type doesn't exist."""

    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Exercise type not found'
    default_code = 'exercise_not_found'


class InvalidExerciseProvider(ExerciseServiceException):
    """Raised when invalid exercise provider is detected."""

    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Invalid exercise provider'
    default_code = 'invalid_exercise_provider'


class TaskGenerationError(ExerciseServiceException):
    """Raised when task generation process fails."""

    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = 'Task generation failed'
    default_code = 'task_generation_error'
