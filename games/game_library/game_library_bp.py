from flask import Blueprint, render_template
from games.adapters.repository import repo_instance
import games.adapters.repository as repo

game_library_bp = Blueprint('game_library_bp', __name__)

@game_library_bp.route('/game_library/<selected_genre>/<selected_publisher>/<current_page>')
def game_library(selected_genre, selected_publisher, current_page):

    current_page = int(current_page)
    items_per_page = 10

    games_dataset = repo.repo_instance.get_games(selected_genre, selected_publisher)

    return render_template(
        'game_library.html',
        selected_genre=selected_genre,
        selected_publisher=selected_publisher,
        current_page=current_page,
        games_dataset=games_dataset[current_page * items_per_page:current_page * items_per_page + items_per_page]
        )
