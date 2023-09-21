from games.adapters.repository import AbstractRepository
from games.domainmodel.model import Review


class NonExistentGameException(Exception):
    pass


class UnknownUserException(Exception):
    pass


def get_game_by_id(game_id, repo: AbstractRepository):
    return repo.get_game_by_id(game_id)


def add_review(game_id: int, rating: int, review_text: str, user_name: str, repo: AbstractRepository):
    game = repo.get_game_by_id(game_id)

    if game is None:
        raise NonExistentGameException

    user = repo.get_user(user_name)

    if user is None:
        raise UnknownUserException

    review = Review(user, game, rating, review_text)

    repo.add_review(review)
