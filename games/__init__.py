"""Initialize Flask app."""

from flask import Flask, render_template


def create_app():
    """Construct the core application."""

    # Create the Flask app object.
    app = Flask(__name__)

    @app.route('/')
    def layout():
        return render_template('index.html')

    @app.route('/game_library')
    def game_library():
        return render_template('game_library.html')

    @app.route('/game_info')
    def game_info():
        return render_template('game_info.html')

    return app
