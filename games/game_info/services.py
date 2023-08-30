from games.adapters.repository import AbstractRepository


def get_game_by_id(game_id, repo: AbstractRepository):
    return repo.get_game_by_id(game_id)
