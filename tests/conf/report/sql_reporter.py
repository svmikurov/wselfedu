"""SQL query reporter with Pydantic config and Rich output.

Features:
- Colorized SQL query output
- Execution time tracking
- Configurable display options
"""

from decimal import Decimal
from typing import Dict, List, Optional

import sqlparse  # type: ignore[import-untyped]
from rich.box import HORIZONTALS
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from ..report.thema import create_theme
from .report_config import ReportConfig


class SQLReporter:
    """Enhanced SQL query reporter with Rich output."""

    def __init__(
        self,
        config: ReportConfig,
        queries: List[Dict[str, str]],
        test_time: Optional[Decimal] = None,
        test_name: Optional[str] = None,
        test_doc: Optional[str] = None,
    ) -> None:
        """Construct the reporter."""
        self.config = config
        self.queries = queries
        self.test_time = test_time
        self.test_name = test_name
        self.test_doc = test_doc
        self.console = Console(theme=create_theme(config))

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
            f'Query: {self.test_doc or self.test_name}',
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

            if self.config.include_sql_query:
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

        if self.test_time and self.config.include_test_time:
            summary_table.add_row(
                'Test execution time:', f'{self.test_time:.3f}s'
            )

        # Print the report
        self.console.print()

        # Print header if enabled
        if self.test_name and self.config.include_test_name:
            # title = f'SQL Queries: {self.test_doc or self.test_name}'
            self.console.rule(style='title', align='left')
            self.console.print()

        # Print queries if enabled
        if self.config.include_sql_query:
            self.console.print(query_table)
            self.console.print()

        # Print summary
        self.console.print(
            Panel(summary_table, title='Summary', border_style='divider')
        )
