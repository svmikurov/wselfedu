"""Defines command to load inial data to database."""

import os.path
from argparse import ArgumentParser
from pathlib import Path
from typing import Any

import yaml
from django.conf import settings
from django.core.management import call_command
from dotenv import load_dotenv
from typing_extensions import override

from .base import CustomBaseCommand

load_dotenv()

BASE_DIR = settings.BASE_DIR

FORCE_PRODUCTION = os.getenv('FORCE_PRODUCTION', 'False').lower() in (
    't',
    '1',
    'true',
)


class Command(CustomBaseCommand):
    """Load initial data into models."""

    fixtures_config_path = 'db/fixtures/fixtures_config.yaml'
    help = 'Load initial data into models'

    def add_arguments(self, parser: ArgumentParser) -> None:
        """Add custom command line args for the management command."""
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
            default=self.fixtures_config_path,
            help='Path to config file',
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

        # Check environment
        if not settings.PRODUCTION:
            self._msg_warning(
                'Not in production! Use FORCE_PRODUCTION=1 to override'
            )
            if not FORCE_PRODUCTION:
                return

        # Check fixture on sensitive
        load_sensitive: bool = bool(options.get('load_sensitive', False))
        if load_sensitive:
            confirm = input("Load SENSITIVE data? (type 'yes' to confirm): ")
            if confirm.lower() != 'yes':
                self._msg_notice('Sensitive data loading cancelled')
                options['load_sensitive'] = False  # type: ignore[assignment]

        # Get fixtures
        try:
            fixtures = config['load_order']
        except (TypeError, KeyError):
            self._msg_error('Error to get fixtures!')
            return

        # Load fixtures
        for fixture in fixtures:
            if 'sensitive/' in fixture and not options['load_sensitive']:
                continue
            self.stdout.write(f'Loading {fixture} ...')

            try:
                load_fixture_options = config['options']
                self._call_load_fixture(fixture, load_fixture_options)
            except Exception as e:
                self._msg_error(f'Error loading {fixture}: {str(e)}')
                if 'sensitive/' in fixture:
                    break

        # Finish message
        self._msg_success('Data loading completed!')

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
        return BASE_DIR / Path(config_path)

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
