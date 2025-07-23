"""Defines simple SQL formatter."""

import logging

import sqlparse  # type: ignore[import-untyped]


class SimpleSQLFormatter(logging.Formatter):
    """SQL formatter."""

    def format(self, record: logging.LogRecord) -> str:
        """Format."""
        if hasattr(record, 'sql'):
            sql = record.sql
            formated: str = sqlparse.format(
                sql, reindent=True, keyword_case='upper'
            )

            return formated
        return ''
