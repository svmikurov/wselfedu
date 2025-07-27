"""Defines SQL executor."""

from pathlib import Path
from sys import stderr, stdout

from django.core.management.base import OutputWrapper
from django.core.management.color import color_style
from django.db import connection

from features.mixins.command import STDCommandMixin


class Executor(STDCommandMixin):
    """SQL command executor."""

    def __init__(self) -> None:
        """Construct the executor."""
        # Console messages components
        self.style = color_style()
        self.stdout = OutputWrapper(stdout)
        self.stderr = OutputWrapper(stderr)

    def read_and_execute(self, script_path: Path) -> None:
        """Read and execute SQL command."""
        print(f'Executing SQL script: "{script_path.name}"')
        try:
            row = self.read_sql_script(script_path)
        except FileNotFoundError:
            self._msg_error(f'Script "{script_path.name}" not executed')
            return
        else:
            self.execute_sql(row)
            self._msg_success(f'Success finished "{script_path.name}" script')

    def read_sql_script(self, script_path: Path) -> str:
        """Read the sql script."""
        try:
            with open(script_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError as e:
            self._msg_error(f'Script "{script_path.name}" not foud')
            raise e

    def execute_sql(self, sql: str) -> None:
        """Execute the scl command."""
        with connection.cursor() as cursor:
            try:
                cursor.execute(sql)
            except Exception as e:
                self._msg_error(f'Failed SQL command: {sql}\nError: {e}')
