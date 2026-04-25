"""Defines simple SQL formatter."""

import logging

import sqlparse


class SimpleSQLFormatter(logging.Formatter):
    """SQL formatter."""

    def format(self, record: logging.LogRecord) -> str:
        """Format SQL query with timestamp."""
        sql = getattr(record, 'sql', record.getMessage())

        formatted_sql = sqlparse.format(
            sql, reindent=True, keyword_case='upper'
        )

        asctime = self.formatTime(record, self.datefmt)

        return (
            f'{asctime} [{record.levelname}] {record.name}\n{formatted_sql}\n'
            f'{"=" * 80}'
        )
