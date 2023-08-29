from flask import Blueprint, render_template, request, redirect, url_for
from games.adapters.repository import repo_instance
import games.game_library.services as services

game_library_bp = Blueprint('game_library_bp', __name__)


@game_library_bp.route('/game_library')
def game_library():

    current_page = request.args.get('current_page')

    current_page = int(current_page)
    items_per_page = 10

    games_dataset = services.get_games_by_genre('all')
    services.alpha_sort_games(games_dataset)

    if current_page < 0:
        current_page = 0
    if current_page * items_per_page > len(games_dataset):
        current_page = len(games_dataset) // items_per_page

    return render_template(
        'game_library.html',
        selected_genre='all',
        current_page=current_page,
        games_dataset=games_dataset[current_page * items_per_page:current_page * items_per_page + items_per_page],
        genres=services.get_genres()
        )


@game_library_bp.route('/game_library/search', methods=['GET', 'POST'])
def game_library_search_term():
    if request.method == 'POST':
        result = request.form
        search_category, search_term = result["search_category"], result["search_term"]
    else:
        search_category = request.args.get("search_category")
        search_term = request.args.get("search_term")

    current_page = request.args.get('current_page')

    current_page = int(current_page)
    items_per_page = 10
    games_dataset = services.get_games_by_search(search_category, search_term)
    services.alpha_sort_games(games_dataset)

    if current_page < 0:
        current_page = 0
    if current_page * items_per_page > len(games_dataset):
        current_page = len(games_dataset) // items_per_page

    return render_template(
        'game_library.html',
        selected_genre='all',
        current_page=current_page,
        games_dataset=games_dataset[current_page * items_per_page:current_page * items_per_page + items_per_page],
        search_category=search_category,
        search_term=search_term,
        genres=services.get_genres()
        )



@game_library_bp.route('/game_library/genre')
def game_library_genre():

    selected_genre = request.args.get('selected_genre')
    current_page = request.args.get('current_page')

    current_page = int(current_page)
    items_per_page = 10

    games_dataset = services.get_games_by_genre(selected_genre)
    services.alpha_sort_games(games_dataset)

    if current_page < 0:
        current_page = 0
    if current_page * items_per_page > len(games_dataset):
        current_page = len(games_dataset) // items_per_page

    genres = services.get_genres()
    services.alpha_sort_genres(genres)

    return render_template(
        'game_library.html',
        selected_genre=selected_genre,
        current_page=current_page,
        games_dataset=games_dataset[current_page * items_per_page:current_page * items_per_page + items_per_page],
        genres=genres
        )

