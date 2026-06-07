"""Flask endpoint."""

from flask import Flask

from wse.di.container import MainContainer

from . import views


def create_app() -> Flask:
    """Create the flask application."""
    container = MainContainer()

    app = Flask(__name__)
    app.container = container  # type: ignore[attr-defined]
    app.add_url_rule('/presentation/', 'presentation', views.presentation)

    return app
