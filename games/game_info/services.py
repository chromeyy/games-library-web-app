import games.adapters.repository as repo

def get_game_by_id(game_id):
    return repo.repo_instance.get_game_by_id(game_id)