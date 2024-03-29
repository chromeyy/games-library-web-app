from flask import Blueprint, render_template, request
import games.game_library.services as services
import games.adapters.repository as repo
game_library_bp = Blueprint('game_library_bp', __name__)


@game_library_bp.route('/game_library')
def game_library():

    current_page = request.args.get('current_page')

    current_page = int(current_page)
    items_per_page = 10
    last_page_number = services.get_last_page_num(services.get_num_of_games_in_genre("all", repo.repo_instance),
                                                  items_per_page)

    if current_page < 0:
        current_page = 0
    if current_page * items_per_page > services.get_num_of_games_in_genre('all', repo.repo_instance):
        current_page = last_page_number

    games_dataset = services.get_games_by_genre('all', current_page, items_per_page, repo.repo_instance)

    genres = services.get_genres(repo.repo_instance)
    services.alpha_sort_genres(genres)

    return render_template(
        'game_library.html',
        selected_genre='all',
        current_page=current_page,
        games_dataset=games_dataset,
        genres=genres,
        last_page_number=last_page_number
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
    last_page_number = services.get_last_page_num(services.get_num_of_games_in_search(search_category, search_term, repo.repo_instance),
                                                  items_per_page)

    if current_page < 0:
        current_page = 0
    if current_page * items_per_page > services.get_num_of_games_in_search(search_category, search_term, repo.repo_instance):
        current_page = last_page_number

    games_dataset = services.get_games_by_search(search_category, search_term, current_page, items_per_page, repo.repo_instance)

    genres = services.get_genres(repo.repo_instance)
    services.alpha_sort_genres(genres)

    return render_template(
        'game_library.html',
        selected_genre='all',
        current_page=current_page,
        games_dataset=games_dataset,
        search_category=search_category,
        search_term=search_term,
        genres=genres,
        last_page_number=last_page_number
        )


@game_library_bp.route('/game_library/genre')
def game_library_genre():

    selected_genre = request.args.get('selected_genre')
    current_page = request.args.get('current_page')

    current_page = int(current_page)
    items_per_page = 10
    last_page_number = services.get_last_page_num(services.get_num_of_games_in_genre(selected_genre, repo.repo_instance), items_per_page)

    if current_page < 0:
        current_page = 0
    if current_page * items_per_page > services.get_num_of_games_in_genre(selected_genre, repo.repo_instance):
        current_page = last_page_number

    games_dataset = services.get_games_by_genre(selected_genre, current_page, items_per_page, repo.repo_instance)

    genres = services.get_genres(repo.repo_instance)
    services.alpha_sort_genres(genres)

    return render_template(
        'game_library.html',
        selected_genre=selected_genre,
        current_page=current_page,
        games_dataset=games_dataset,
        genres=genres,
        last_page_number=last_page_number
        )
