"""Flask app views."""

from __future__ import annotations

from typing import TYPE_CHECKING

from dependency_injector.wiring import Provide, inject
from flask import render_template

from wse.di.container import MainContainer

if TYPE_CHECKING:
    from wse.application.abstract import AbstractCreateTaskUseCase
    from wse.domain.protocols import Presentable


@inject
def presentation(
    use_case: AbstractCreateTaskUseCase[Presentable] = Provide[
        MainContainer.applications.create_presentation_use_case
    ],
) -> str:
    """Render the item study presentation task."""
    task = use_case.execute()
    return render_template(
        'task.html',
        task=task,
    )
