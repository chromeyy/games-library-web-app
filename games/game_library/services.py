import games.adapters.repository as repo

def get_games_by_genre(genre):
    return repo.repo_instance.get_games_by_genre(genre)

def get_games_by_search(search_category, search_term):
    return repo.repo_instance.get_games_by_search(search_category, search_term)

def get_genres():
    return repo.repo_instance.get_genres()

def alpha_sort_games(games):
    games.sort(key=lambda game: game.title)