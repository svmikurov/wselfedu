"""SQL query reporter with Pydantic config and Rich output.

Features:
- Colorized SQL query output
- Execution time tracking
- Configurable display options
"""

from decimal import Decimal
from timeit import default_timer as timer

import sqlparse  # type: ignore[import-untyped]
import yaml
from django.conf import settings
from django.db import connection
from rich.box import HORIZONTALS
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from utils.sql.report_config import ReportConfig
from utils.sql.thema import create_theme

CONFIG_PATH = settings.BASE_DIR / 'tests' / 'conf' / 'test_config.yml'
CONFIG = ReportConfig(**yaml.safe_load(open(CONFIG_PATH)))


class SQLReporter:
    """Enhanced SQL query reporter with Rich output."""

    def __init__(
        self,
        test_time: Decimal | None = None,
        test_name: str | None = None,
        test_doc: str | None = None,
    ) -> None:
        """Construct the reporter."""
        self._test_name = test_name
        self._total_test_time: Decimal | None = test_time
        self._test_doc = test_doc

        self._start_time: Decimal | None = None
        self._config = CONFIG
        self._console = Console(theme=create_theme(self._config))
        self._queries: list[dict[str, str]] = []

    @staticmethod
    def format_sql(sql: str) -> str:
        """Format SQL query with sqlparse."""
        return str(sqlparse.format(sql, reindent=True, keyword_case='upper'))

    def print_report(self) -> None:
        """Generate and print the full report."""
        # Prepare statistics
        stats = {
            'sql_count': Decimal(0),
            'savepoint_count': Decimal(0),
            'total_time': Decimal(0),
        }

        # Create main table for queries
        query_table = Table(
            title='SQL Query Report',
            show_header=True,
            header_style='title',
            box=HORIZONTALS,  # Add horizontal lines
            show_lines=True,  # Lines between rows
            padding=(0, 1),
        )
        query_table.add_column(
            f'Query: {self._test_doc or self._test_name}',
            style='sql',
        )
        query_table.add_column(
            'Time (s)',
            style='time',
            justify='right',
        )

        # Process each query
        for query in self.queries:
            sql, time = query['sql'], Decimal(query['time'])
            stats['total_time'] += time

            if 'SAVEPOINT' in sql:
                stats['savepoint_count'] += 1
                style = 'savepoint'
            else:
                stats['sql_count'] += 1
                style = 'sql'

            if self._config.include_sql_query:
                query_table.add_row(
                    Text(self.format_sql(sql), style=style),
                    Text(f'{time:.3f}', style='time'),
                )

        # Create summary table
        summary_table = Table.grid(padding=(0, 2))
        summary_table.add_column(style='default')
        summary_table.add_column(style='default')

        summary_table.add_row('SQL queries:', str(stats['sql_count']))
        summary_table.add_row('Savepoints:', str(stats['savepoint_count']))
        summary_table.add_row(
            'Total queries:',
            str(stats['sql_count'] + stats['savepoint_count']),
        )
        summary_table.add_row(
            'Total query time:', f'{stats["total_time"]:.3f}s'
        )

        if self._total_test_time and self._config.include_test_time:
            summary_table.add_row(
                'Test execution time:', f'{self._total_test_time:.3f}s'
            )

        # Print the report
        self._console.print()

        # Print header if enabled
        if self._test_name and self._config.include_test_name:
            # title = f'SQL Queries: {self.test_doc or self.test_name}'
            self._console.rule(style='title', align='left')
            self._console.print()

        # Print queries if enabled
        if self._config.include_sql_query:
            self._console.print(query_table)
            self._console.print()

        # Print summary
        self._console.print(
            Panel(summary_table, title='Summary', border_style='divider')
        )

    # API

    def start_act(self) -> None:
        """Start act of test."""
        self._start_timer()
        self.clear_queries()

    def end_act(self) -> None:
        """End act of test."""
        self._stop_timer()
        self._queries = [*connection.queries]
        self.clear_queries()

    @staticmethod
    def clear_queries() -> None:
        """Clear the queries."""
        connection.queries.clear()

    @property
    def queries(self) -> list[dict[str, str]]:
        """Get queries."""
        return self._queries

    # Timeout management

    def _start_timer(self) -> None:
        self._start_time = Decimal(timer())

    def _stop_timer(self) -> None:
        if self._start_time is None:
            raise RuntimeError('The timer was not started to stop')
        self._total_test_time = Decimal(timer()) - self._start_time
