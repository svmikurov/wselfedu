from dataclasses import dataclass
from typing import Any


@dataclass
class TaskData:
    """Класс для хранения данных упражнения изучения слов."""

    lookup_parameters: Any
