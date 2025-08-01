"""Defines command to load inial data to database."""

from argparse import ArgumentParser, RawDescriptionHelpFormatter
from pathlib import Path
from typing import Any

import yaml
from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand
from typing_extensions import override

from apps.core.mixins.command import DjangoStyledMessageMixin
from utils.load import get_boolean_value

PRODUCTION: bool = get_boolean_value('PRODUCTION')
FORCE_PRODUCTION: bool = get_boolean_value('FORCE_PRODUCTION')
FIXTURES_CONFIG_PATH = 'db/fixtures/fixtures_config.yaml'
DESCRIPTION = """
Command to load initial data into the database
----------------------------------------------

    If the production environment is not set, sensitive data (user, ...)
    is loaded from the /sensitive/ fixtures directory by default.

    To load sensitive data in production, set environment
    FORCE_PRODUCTION=1.

    To load fixtures uses load fixture config.
    For example:

        db/fixtures/fixtures_config.yaml:

            load_order:
              - db/fixtures/public/apps.json
              - db/fixtures/public/math_exercise.json
              - db/fixtures/sensitive/users.json

            options:
              default_database: "default"
              ignore_nonexistent: false
"""


class Command(DjangoStyledMessageMixin, BaseCommand):
    """Load initial data into models."""

    help = 'Load initial data into models'
    success_load = True

    def add_arguments(self, parser: ArgumentParser) -> None:
        """Add custom command line args for the management command."""
        parser.formatter_class = RawDescriptionHelpFormatter
        parser.description = DESCRIPTION

        parser.add_argument(
            '--load-sensitive',
            action='store_true',
            dest='load_sensitive',
            default=False,
            help='Load sensitive data (requires confirmation)',
        )
        parser.add_argument(
            '--config',
            type=str,
            dest='config_path',
            default=FIXTURES_CONFIG_PATH,
            help='Path to load fixtures configuration file',
        )

    @override
    def handle(self, *args: object, **options: dict[str, Any]) -> None:  # noqa: C901
        """Handle the command with proper type safety."""
        # Get config to load fixtures
        config_path = self._get_config_path(options)
        config = self._read_config(config_path)
        if config is None:
            self._msg_error('Load fixtures config not set')
            return

        # Check environment before load fixtures
        if settings.PRODUCTION:
            self._msg_warning(
                'Not in production! Use FORCE_PRODUCTION=1 to override'
            )
            if not FORCE_PRODUCTION:
                return

        # Set load fixture options for sensitive fixture loading
        load_sensitive: bool = bool(options.get('load_sensitive', False))
        if load_sensitive and PRODUCTION:
            confirm = input("Load SENSITIVE data? (type 'yes' to confirm): ")

            if confirm.lower() != 'yes':
                self._msg_notice('Sensitive data loading cancelled')
                options['load_sensitive'] = False  # type: ignore[assignment]

        else:
            self._msg_warning('Sensitive data loading enable')
            options['load_sensitive'] = True  # type: ignore[assignment]

        # Get fixture paths to load
        try:
            fixtures: list[Path] = config['load_order']
        except (TypeError, KeyError):
            self._msg_error('Error to get fixtures!')
            return

        # Load fixtures
        for fixture in fixtures:
            if 'sensitive' in str(fixture):
                if not options['load_sensitive']:
                    continue
                self._msg_warning(f'Loading sensitive {fixture} ...')
            else:
                print(f'Loading {fixture} ...')

            try:
                load_fixture_options = config['options']
                self._call_load_fixture(fixture, load_fixture_options)
            except Exception as e:
                self._msg_error(f'Error loading {fixture}: {str(e)}')
                self.success_load = False

        # Finish message
        if self.success_load:
            self._msg_success('Initial data loading into models completed!')
        else:
            self._msg_error('Error load initial data into models')

    # Utility methods

    @staticmethod
    def _get_config_path(options: dict[str, Any]) -> Path:
        """Extract config path from options with type safety."""
        config_path = options.get('config_path')
        if not isinstance(config_path, (str, Path)):
            raise ValueError(
                f'Expected config path type `str` or `Path`, '
                f'got `{type(config_path)}`'
            )
        return settings.BASE_DIR / Path(config_path)

    def _read_config(self, config_path: Path) -> dict[str, Any] | None:
        """Safely open and parse config file."""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config: dict[str, Any] = yaml.safe_load(f)
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR('Config file not found!'))
            return None
        else:
            return config

    @staticmethod
    def _call_load_fixture(path: Path, options: dict[str, Any]) -> None:
        """Call command to load fixture."""
        call_command(
            'loaddata',
            path,
            database=options.get('default', 'default'),
            ignorenonexistent=options.get('ignore_nonexistent', False),
            verbosity=1,
        )
