"""Defines command to DB initialisation."""

from pathlib import Path

import sqlparse  # type: ignore[import-untyped]
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import connection

script_dir = settings.BASE_DIR / 'db' / 'sql' / 'init'

scripts: list[Path] = [
    script_dir / '003_initial_shema.sql',
]


def execute_sql(sql: str) -> None:
    """Execute SQL command."""
    with connection.cursor() as cursor:
        try:
            cursor.execute(sql)
        except Exception as e:
            raise Exception(f'Failed SQL command: {sql}\nError: {e}') from e


def reade_sql_script(path: Path | str) -> str:
    """Return SQL row."""
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def format_sql(row: str) -> list[str]:
    """Return split SQL commands."""
    sql: list[str] = sqlparse.split(row)
    return sql


class Command(BaseCommand):
    """Database initialization command."""

    help = 'Initialization of database'

    def handle(self, *args: object, **options: object) -> None:
        """Handle the command."""
        for script in scripts:
            print(f'Executing SQL script {script}')
            try:
                raw = reade_sql_script(script)
            except FileNotFoundError:
                self.stdout.write(
                    self.style.ERROR(f"Script '{script.name}' not foud")
                )
                return

            sql_commands = format_sql(raw)

            for sql in sql_commands:
                execute_sql(sql)

            self.stdout.write(
                self.style.SUCCESS(f"Success finished '{script}' script")
            )
