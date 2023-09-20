from games.adapters.repository import AbstractRepository


def get_user(user_name, repo: AbstractRepository):
    return repo.get_user(user_name)