from games.adapters.database_repository import SqlAlchemyRepository
from games.domainmodel.model import User, Review, Game, Genre, Publisher


# USER TESTS
def test_repository_can_add_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = User('Victor', 'password')
    repo.add_user(user)

    user2 = User('Tomato', 'password')
    repo.add_user(user2)

    user3 = repo.get_user('Victor')

    assert user3 == user and user3 is user

def test_repository_can_get_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = repo.get_user('tori')
    assert user == User('tori', '@Vrya365')


def test_repository_can_update_a_user(session_factory): # TO DO
    pass

def test_repository_does_not_retrieve_a_non_existent_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = repo.get_user('PotatoMan')
    assert user is None

def test_repository_can_get_list_of_users(session_factory):  #NOT COMPLETE
    repo = SqlAlchemyRepository(session_factory)
    users = repo.get_users()
    assert len(users) == xxx #DOTHIS

# REVIEW TESTS
def test_repository_can_add_review(session_factory): #DID NOT DO GAME PROPERLY
    repo = SqlAlchemyRepository(session_factory)

    review = Review(
        'tori',
        'game',
        '4',
        'this is great!'
    )

def test_repository_can_get_reviews(session_factory): #NOT COMPLETE
    repo = SqlAlchemyRepository(session_factory)
    reviews = repo.get_reviews()
    assert len(reviews) == xxx # TO DO


def test_repository_game_has_review(session_factory):# TO DO
    pass

def test_repository_user_has_review(session_factory):# TO DO
    pass

# GAME TESTS
def test_repository_can_add_game(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    game = Game(80085, 'test_game')
    repo.add_games(game)

    game2 = Game(80086, 'test_game_2')
    repo.add_games(game2)

    assert repo.get_game_by_id(80085) == game

def test_repository_does_not_get_a_non_existent_game(session_factory):
    pass

def test_repository_can_get_games_by_ids(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    game = Game(80085, 'test_game')
    repo.add_games(game)

    assert repo.get_game_by_id(80085) == game

def test_repository_does_not_get_games_for_non_existent_id(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    game = repo.get_game_by_id(19247333348175192)
    assert game is None

def test_repository_can_get_games_by_genre(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    game = Game(80085, 'test_game')
    game.add_genre(Genre('Horror'))
    repo.add_games(game)


    assert game in repo.get_games_by_genre('Horror')

def test_repository_returns_an_empty_list_for_non_existent_genre(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    games_list = repo.get_games_by_genre('test_fake_genre12345')
    assert games_list is None

def test_repository_can_get_games_by_publisher(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    game = Game(80085, 'test_game')
    game.publisher = (Publisher('test_publisher'))
    repo.add_games(game)

    assert game in repo.get_games_by_publisher('test_publisher')


def test_repository_returns_an_empty_list_for_non_existent_publisher(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    games_list = repo.get_games_by_publisher('test_fake_publisher12345')
    assert games_list is None

def test_repository_can_get_games_by_search(session_factory): # TO DO
    repo = SqlAlchemyRepository(session_factory)

    game = Game(80085, 'test_game')
    repo.add_games(game)

    assert game in repo.get_games_by_search('test_game')

def test_repository_returns_an_empty_list_for_non_existent_search(session_factory): # TO DO
    repo = SqlAlchemyRepository(session_factory)
    games_list = repo.get_games_by_search('test_fake_game12345')
    assert games_list is None

# GENRE TESTS
def test_repository_can_add_a_genre(session_factory): # CHECK
    repo = SqlAlchemyRepository(session_factory)
    game = Game(80085, 'test_game')
    repo.add_games(game)

    genre2 = Genre('test2')
    game.add_genre(genre2)

    genres = game.genres

    assert genre2 is Genre and genre2 == game.genres[1]

def test_repository_can_get_a_genre(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    game = Game(80085, 'test_game')
    repo.add_games(game)

    genre1 = Genre('test1')
    game.add_genre(genre1)

    assert game.genres[0] == genre1 and game.genres[0] is Genre

def test_repository_can_get_list_of_genres(session_factory): # CHECK
    repo = SqlAlchemyRepository(session_factory)
    game = Game(80085, 'test_game')
    repo.add_games(game)

    genre1 = Genre('test1')
    game.add_genre(genre1)

    assert len(game.genres[0]) == 1
