"""Initialize Flask app."""

from pathlib import Path
import games.adapters.repository as repo
from games.adapters.memory_repository import MemoryRepository, populate

from flask import Flask, render_template, Blueprint
from .blueprints.index_bp import index_bp
from .blueprints.game_library_bp import game_library_bp
from .blueprints.game_info_bp import game_info_bp



def create_app():
    """Construct the core application."""

    # Create the Flask app object.
    app = Flask(__name__)

    data_path = Path('games') / 'adapters' / 'data'

    repo.repo_instance = MemoryRepository()
    populate(data_path, repo.repo_instance)

    app.register_blueprint(index_bp)
    app.register_blueprint(game_library_bp)
    app.register_blueprint(game_info_bp)

    return app
