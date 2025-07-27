"""Defines command to DB initialisation."""

import yaml
from django.conf import settings
from django.core.management import BaseCommand

from features.mixins.command import STDCommandMixin
from utils.sql.executor import Executor

from .command_config import MainCommandConfig

SQL_SCRIPTS_DIR = settings.BASE_DIR / 'db' / 'sql' / 'init'
SQL_TABLE_SCRIPTS_PATH = SQL_SCRIPTS_DIR / 'order.yml'

CONFIG = MainCommandConfig(**yaml.safe_load(open(SQL_TABLE_SCRIPTS_PATH)))


class Command(STDCommandMixin, BaseCommand):
    """Database initialization command."""

    help = 'Initialization of database'

    def handle(self, *args: object, **options: object) -> None:
        """Handle the command."""
        executor = Executor()
        for script in CONFIG.sql_execute_order:
            script_path = SQL_SCRIPTS_DIR / script
            executor.read_and_execute(script_path)
