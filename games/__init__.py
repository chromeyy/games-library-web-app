"""Initialize Flask app."""

from pathlib import Path
import games.adapters.repository as repo
from games.adapters.memory_repository import MemoryRepository
from games.adapters.repository_populate import populate

from flask import Flask


def create_app(test_config=None):
    """Construct the core application."""

    # Create the Flask app object.
    app = Flask(__name__)

    # Configure the app from configuration-file settings.
    app.config.from_object('config.Config')

    data_path = Path('games') / 'adapters' / 'data'

    if test_config is not None:
        # Load test configuration, and override any configuration settings.
        app.config.from_mapping(test_config)
        data_path = app.config['TEST_DATA_PATH']

    # Create the MemoryRepository implementation for a memory-based repository.
    repo.repo_instance = MemoryRepository()
    # fill in the content of the repository from the provided csv files
    populate(data_path, repo.repo_instance)

    # Build the application - these steps require an application context.
    with app.app_context():
        # Register blueprints.
        from games.index.index_bp import index_bp
        app.register_blueprint(index_bp)

        from games.game_library.game_library_bp import game_library_bp
        app.register_blueprint(game_library_bp)

        from games.game_info.game_info_bp import game_info_bp
        app.register_blueprint(game_info_bp)

        from games.authentication.authentication_bp import authentication_bp
        app.register_blueprint(authentication_bp)

        from games.user_info.user_info_bp import user_info_bp
        app.register_blueprint(user_info_bp)

    return app
