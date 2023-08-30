from games.adapters.repository import AbstractRepository


def get_games_by_genre(genre, current_page, items_per_page, repo: AbstractRepository):
    games = repo.get_games_by_genre(genre)
    alpha_sort_games(games)
    return games[current_page * items_per_page:current_page * items_per_page + items_per_page]


def get_games_by_search(search_category, search_term, current_page, items_per_page, repo: AbstractRepository):
    games = repo.get_games_by_search(search_category, search_term)
    alpha_sort_games(games)
    return games[current_page * items_per_page:current_page * items_per_page + items_per_page]


def get_genres(repo: AbstractRepository):
    return repo.get_list_of_genres()


def get_num_of_games_in_genre(genre, repo: AbstractRepository):
    return len(repo.get_games_by_genre(genre))


def get_num_of_games_in_search(search_category, search_term, repo: AbstractRepository):
    return len(repo.get_games_by_search(search_category, search_term))


def get_last_page_num(num_of_games, items_per_page):
    return num_of_games // items_per_page


def get_num_of_genres(repo: AbstractRepository):
    return len(repo.get_list_of_genres())


def alpha_sort_games(games):
    games.sort(key=lambda game: game.title)


def alpha_sort_genres(genres):
    genres.sort(key=lambda genre: genre.genre_name)