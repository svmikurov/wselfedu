"""Defines third-party logger handler."""

import logging
from typing import TextIO


class ColorfulSQLHandler(logging.StreamHandler[TextIO]):
    """Colore SQL output handler."""

    def emit(self, record: logging.LogRecord) -> None:
        """Handel."""
        try:
            message = self.format(record)
            if hasattr(record, 'sql') or record.getMessage().startswith('('):
                message = f'\033[36m{message}\033[0m'
            self.stream.write(message + '\n')
            self.flush()
        except Exception as e:
            print(f'Logging error: {str(e)}')
            super().handleError(record)
