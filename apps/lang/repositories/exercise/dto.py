"""Exercise DTO."""

from pydantic import BaseModel

from apps.lang.schemas import LookupCondition, SettingsModel


class RegularParameters(BaseModel):
    """Regular exercise parameters."""

    conditions: LookupCondition | None
    settings: SettingsModel | None
