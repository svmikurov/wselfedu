"""Defines SQL formater."""

import logging


class SQLFormatter(logging.Formatter):
    """SQL formatter."""

    def format(self, record: logging.LogRecord) -> str:
        """Format."""
        # For regular SQL queries
        if hasattr(record, 'sql'):
            sql = record.sql
            duration = getattr(record, 'duration', 0)

            sql = sql.replace('"', '')
            sql = ' '.join(sql.split())

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

        return super().format(record)
