"""Defines report configuration."""

from typing import Optional

from pydantic import BaseModel, Field


class ReportConfig(BaseModel):
    """Configuration model for SQL reporting."""

    no_color: str = Field('default', description='Default color for text')
    savepoint_color: str = Field(
        'yellow', description='Color for savepoint queries'
    )
    sql_color: str = Field('cyan', description='Color for SQL queries')
    time_color: str = Field('green', description='Color for time values')
    title_color: str = Field('blue', description='Color for titles')
    outer_divider_color: str = Field(
        'magenta', description='Color for dividers'
    )
    include_sql_query: bool = Field(
        True, description='Show SQL queries in output'
    )
    include_test_time: bool = Field(True, description='Show total test time')
    include_test_name: bool = Field(
        True, description='Show test name in header'
    )
    bottom_outer_divider: bool = Field(True, description='Show footer divider')
    divider_length: int = Field(80, gt=0, description='Divider length')
    output_file: Optional[str] = Field(
        default=None, description="Path to output file (None for console only)"
    )
