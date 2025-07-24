"""Defines command to DB initialisation."""

import sqlparse  # type: ignore[import-untyped]
import yaml
from django.conf import settings
from django.db import connection

from .base import CustomBaseCommand
from .command_config import MainCommandConfig

SQL_SCRIPTS_DIR = settings.BASE_DIR / 'db' / 'sql' / 'init'
SQL_TABLE_SCRIPTS_PATH = SQL_SCRIPTS_DIR / 'order.yml'

CONFIG = MainCommandConfig(**yaml.safe_load(open(SQL_TABLE_SCRIPTS_PATH)))


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
        for script in CONFIG.sql_execute_order:
            script_path = SQL_SCRIPTS_DIR / script
            print(f'Executing SQL script {script_path}')

            try:
                with open(script_path, 'r', encoding='utf-8') as f:
                    row = f.read()

            except FileNotFoundError:
                self._msg_error(f"Script '{script_path.name}' not foud")
                return

            sql_commands = sqlparse.split(row)

            # Execute SQL command
            for sql in sql_commands:
                execute_sql(sql)

            self._msg_success(f"Success finished '{script_path.name}' script")
