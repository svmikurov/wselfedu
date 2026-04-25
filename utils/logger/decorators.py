"""Logger for file errors."""

import functools
import logging
from typing import Any, Callable, TypeVar

F = TypeVar('F', bound=Callable[..., Any])


# FIXME: Fix type ignore
def log_errors_to_file(logger_name: str | None = None) -> Callable[..., Any]:
    """Decorate to log exceptions to file without console output."""

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: object, **kwargs: object) -> Callable[..., Any]:
            logger = logging.getLogger(logger_name or 'decorated_error_file')

            try:
                return func(*args, **kwargs)  # type: ignore

            except Exception as exc:
                logger.exception(exc)
                raise

        return wrapper  # type: ignore

    return decorator
