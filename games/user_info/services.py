from games.adapters.repository import AbstractRepository


def get_user(username, repo: AbstractRepository):
    return repo.get_user(username)