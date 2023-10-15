from games.adapters.database_repository import SqlAlchemyRepository
from games.domainmodel.model import User, Review, Game, Genre, Publisher


# USER TESTS
def test_repository_can_add_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = User('Dave', '123456789')
    repo.add_user(user)

    repo.add_user(User('Martin', '123456789'))

    user2 = repo.get_user('Dave')

    assert user2 == user and user2 is user


def test_repository_can_get_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = repo.get_user('tori')
    assert user == User('tori', '@Vrya365')


def test_repository_does_not_retrieve_a_non_existent_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = repo.get_user('PotatoMan')
    assert user is None


# REVIEW TESTS
def test_repository_can_get_add_review(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    reviews = repo.get_reviews()
    assert len(reviews) == 3

    test_user = repo.get_user('tom')
    test_game = repo.get_game_by_id(7940)
    review = Review(test_user, test_game, 1, "test_comment")
    repo.add_review(review)

    reviews = repo.get_reviews()

    assert len(reviews) == 4
    assert test_user.reviews[-1] == review
    assert test_game.reviews[-1] == review


# GAME TESTS
def test_repository_can_add_game(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    game = Game(80085, 'test_game')
    game.release_date = "Oct 18, 2003"
    game.price = float(5)
    game.description = "test desc"
    game.image_url = "url"
    publisher = Publisher("testPub")
    game.publisher = publisher
    genre = Genre("testGenre")
    game.add_genre(genre)

    repo.add_games(game)

    assert repo.get_game_by_id(80085) == game


def test_repository_does_not_get_a_non_existent_game(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    assert repo.get_game_by_id(666999) is None


def test_repository_can_get_games_by_ids(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    assert repo.get_game_by_id(267360).title == 'MURI'


def test_repository_does_not_get_games_for_non_existent_id(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    game = repo.get_game_by_id(19247333348175192)
    assert game is None


def test_repository_can_get_games_by_genre(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    assert len(repo.get_games_by_genre('RPG')) == 131
    assert len(repo.get_games_by_genre('fake')) == 0
    assert repo.get_game_by_id(7940) in repo.get_games_by_genre('Action')


def test_repository_can_get_games_by_search(session_factory): # TO DO
    repo = SqlAlchemyRepository(session_factory)
    game = repo.get_game_by_id(7940)

    assert game in repo.get_games_by_search("Title", "call")
    assert game in repo.get_games_by_search("Publisher", "Act")
    assert len(repo.get_games_by_search("Title", "the")) == 107
    assert len(repo.get_games_by_search("Genre", "RPG")) == 131
    assert len(repo.get_games_by_search("Publisher", "ac")) == 60
    assert len(repo.get_games_by_search("Publisher", "does-not-exist")) == 0


# GENRE TESTS
def test_repository_can_get_list_of_genres(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    assert len(repo.get_list_of_genres()) == 24

    repo.add_genre(Genre("test_genre"))
    assert len(repo.get_list_of_genres()) == 25