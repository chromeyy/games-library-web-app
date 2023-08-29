from flask import Blueprint, render_template, request
from games.adapters.repository import repo_instance
import games.adapters.repository as repo

game_library_bp = Blueprint('game_library_bp', __name__)


@game_library_bp.route('/game_library')
def game_library():

    current_page = request.args.get('current_page')

    current_page = int(current_page)
    items_per_page = 10

    games_dataset = repo.repo_instance.get_games_by_genre('all')

    return render_template(
        'game_library.html',
        selected_genre='all',
        current_page=current_page,
        games_dataset=games_dataset[current_page * items_per_page:current_page * items_per_page + items_per_page]
        )


@game_library_bp.route('/game_library/search', methods=['GET', 'POST'])
def game_library_search_term():
    if request.method == 'POST':
        result = request.form

        current_page = request.args.get('current_page')

        current_page = int(current_page)
        items_per_page = 10
        games_dataset = repo.repo_instance.get_games_by_search(result["search_category"], result["search_term"])

        return render_template(
            'game_library.html',
            selected_genre='all',
            current_page=current_page,
            games_dataset=games_dataset[current_page * items_per_page:current_page * items_per_page + items_per_page],
            result=result
            )


@game_library_bp.route('/game_library/genre')
def game_library_genre():

    selected_genre = request.args.get('selected_genre')
    current_page = request.args.get('current_page')

    current_page = int(current_page)
    items_per_page = 10

    games_dataset = repo.repo_instance.get_games_by_genre(selected_genre)

    return render_template(
        'game_library.html',
        selected_genre=selected_genre,
        current_page=current_page,
        games_dataset=games_dataset[current_page * items_per_page:current_page * items_per_page + items_per_page]
        )

