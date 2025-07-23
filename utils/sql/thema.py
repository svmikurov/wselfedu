"""Defines report layout."""

from rich.theme import Theme

from utils.sql.report_config import ReportConfig


def create_theme(config: ReportConfig) -> Theme:
    """Create Rich theme from config."""
    return Theme(
        {
            'sql': config.sql_color,
            'time': config.time_color,
            'title': config.title_color,
            'savepoint': config.savepoint_color,
            'divider': config.outer_divider_color,
            'default': config.no_color,
        }
    )
