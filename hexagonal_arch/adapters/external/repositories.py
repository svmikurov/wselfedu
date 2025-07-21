"""Defines external repository adapter."""

from ...ports.external import IHistoryRepository


class PostgresHistoryRepository(IHistoryRepository):
    """Postgres storage."""

    def save(self, operation: str, a: float, b: float, result: float) -> None:
        """Save to postgres database."""
        query = 'INSERT INTO history VALUES (%s, %s, %s, %s)'
        print(query, (operation, a, b, result))
