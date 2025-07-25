"""Defines SQL formater."""

import logging
from typing import TextIO


class SQLFormatter(logging.Formatter):
    """SQL formatter."""

    def format(self, record: logging.LogRecord) -> str:
        """Format."""
        # For regular SQL queries
        if hasattr(record, 'sql'):
            sql = record.sql
            duration = getattr(record, 'duration', 0)

            # Форматируем SQL
            sql = sql.replace('"', '')  # Убираем кавычки
            sql = ' '.join(sql.split())  # Убираем лишние пробелы

            if hasattr(record, 'params') and record.params:
                try:
                    sql = sql % record.params
                except Exception:
                    pass

            return f'SQL ({duration:.3f}s): {sql}'

        # For transaction messages (BEGIN, COMMIT, etc.)
        elif record.getMessage().startswith('('):
            try:
                parts = record.getMessage().split(';')
                time_part = parts[0].strip('()').split()
                duration = float(time_part[0])
                operation = time_part[1]
                return f'TRANSACTION ({duration:.3f}s): {operation}'
            except Exception:
                return super().format(record)

        # Для всех остальных сообщений
        return super().format(record)


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
