"""Initialize Flask app."""

from flask import Flask, render_template, Blueprint
from .blueprints.index_bp import index_bp
from .blueprints.game_library_bp import game_library_bp
from .blueprints.game_info_bp import game_info_bp


def create_app():
    """Construct the core application."""

    # Create the Flask app object.
    app = Flask(__name__)

    app.register_blueprint(index_bp)
    app.register_blueprint(game_library_bp)
    app.register_blueprint(game_info_bp)

    return app
