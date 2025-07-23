"""Defines SQL parse components.

Provides to console output a SQL queries from tests:
    - single query text
    - single query time execution
    - combined queries time execution
    - test time execution
"""

from decimal import Decimal

import sqlparse  # type: ignore[import-untyped]
from termcolor import colored

from tests.conf.utils.config_utils import load_config

conf = load_config()

NO_COLOR = conf['no_color']
SAVEPOINT_COLOR = conf['savepoint_color']
SQL_COLOR = conf['sql_color']
TIME_COLOR = conf['time_color']
TITLE_COLOR = conf['title_color']
OUTER_DIVIDER_COLOR = conf['outer_divider_color']
INCLUDE_SQL_QUERY = conf.get('include_sql_query', False) is True
INCLUDE_TEST_TIME = conf.get('include_test_time', False) is True
INCLUDE_TEST_NAME = conf.get('include_test_name', False) is True
BOTTOM_OUTER_DIVIDER = conf.get('bottom_outer_divider', False) is True


def _color(text: str | int | Decimal, color: str | None = None) -> str:
    """Color the text."""
    if color is not None:
        return colored(text, color)
    return str(text)


def _format(sql: str) -> str:
    """Format SQL."""
    return str(sqlparse.format(sql, reindent=True, keyword_case='upper'))


def _divider(
    char: str = '-',
    length: int = conf['divider_length'],
    color: str | None = None,
) -> str:
    line = char * length
    return _color(line, color)


class SQLOutput:
    """Output SQL query with time executing."""

    def __init__(
        self,
        queries: list[dict[str, str]],
        test_time: int | float | Decimal | None = None,
        test_name: str | None = None,
        test_doc: str | None = None,
    ) -> None:
        """Construct the output."""
        self._queries = queries
        self._test_time = test_time
        self._test_name = test_name
        self._test_doc = test_doc

    def output_sql(self) -> None:
        """Output SQL queries."""
        sql_query_counter = 0
        save_point_counter = 0
        total_query_time = Decimal()

        report: list[str] = [_divider('=', color=OUTER_DIVIDER_COLOR)]

        if INCLUDE_TEST_NAME:
            report.append(self.formated_title)
            report.append(_divider(color=OUTER_DIVIDER_COLOR))

        for query in self._queries:
            sql, time = query['sql'], query['time']
            line_color: str | None = NO_COLOR
            time_color: str | None = TIME_COLOR

            if 'SAVEPOINT' in sql:
                line_color = SAVEPOINT_COLOR
                time_color = NO_COLOR

                save_point_counter += 1
            else:
                sql_query_counter += 1

            total_query_time += Decimal(time)

            if INCLUDE_SQL_QUERY:
                time_string = f'Time: {_color(time, time_color)}s'

                report.append(_color(_format(sql), line_color))
                report.append(_color(time_string, line_color))
                report.append(_divider())

        report[-1] = _color(report[-1], color=OUTER_DIVIDER_COLOR)
        report.append(
            f'SQL query count:           {_color(sql_query_counter)}'
        )
        report.append(
            f'Save point query count:    {_color(save_point_counter)}'
        )
        report.append(
            f'Total query count:'
            f'         {_color(sql_query_counter + save_point_counter)}'
        )
        report.append(
            f'Total query time:          {_color(total_query_time)}s'
        )

        if self._test_time is not None and INCLUDE_TEST_TIME:
            formated_sql = _color(f'{Decimal(self._test_time):.3f}')
            report.append(f'Total test execution time: {formated_sql}s')

        if BOTTOM_OUTER_DIVIDER:
            report.append(_divider('=', color=OUTER_DIVIDER_COLOR))

        print()
        print(*report, sep='\n')

    @property
    def test_name(self) -> str:
        """Get the test name."""
        return self._test_name + '.py' if self._test_name is not None else ''

    @property
    def test_doc(self) -> str:
        """Get the test docstring."""
        return self._test_doc if self._test_doc is not None else self.test_name

    @property
    def formated_title(self) -> str:
        """Get the formated title."""
        title = 'SQL queries: %s'
        colored_test_name = _color(self.test_doc, TITLE_COLOR)
        return title % colored_test_name
