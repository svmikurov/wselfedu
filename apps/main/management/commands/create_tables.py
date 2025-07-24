"""Defines command to DB initialisation."""

from pathlib import Path

import sqlparse  # type: ignore[import-untyped]
from django.conf import settings
from django.db import connection

from .base import CustomBaseCommand

SCRIPT_DIR = settings.BASE_DIR / 'db' / 'sql' / 'init'

scripts: list[Path] = [
    SCRIPT_DIR / '003_initial_shema.sql',
]


def execute_sql(sql: str) -> None:
    """Execute SQL command."""
    with connection.cursor() as cursor:
        try:
            cursor.execute(sql)
        except Exception as e:
            raise Exception(f'Failed SQL command: {sql}\nError: {e}') from e


class Command(CustomBaseCommand):
    """Database initialization command."""

    help = 'Initialization of database'

    def handle(self, *args: object, **options: object) -> None:
        """Handle the command."""
        for script_path in scripts:
            print(f'Executing SQL script {script_path}')
            
            try:
                with open(script_path, 'r', encoding='utf-8') as f:
                    raw = f.read()
            
            except FileNotFoundError:
                self._msg_error(f"Script '{script_path.name}' not foud")
                return

            sql_commands = sqlparse.split(raw)

            # Execute SQL command
            for sql in sql_commands:
                execute_sql(sql)

            self._msg_success(f"Success finished '{script_path.name}' script")
