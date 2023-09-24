import pytest

from games.domainmodel.model import *

from games.authentication.services import AuthenticationException

from games.game_info import services as games_info_services
from games.game_library import services as games_library_services
from games.authentication import services as auth_services
from games.user_info import services as user_info_services


@pytest.fixture()
def list_of_games():
    return [Game(1, "A"), Game(4, "D"), Game(3, "C"), Game(2, "B")]


@pytest.fixture()
def list_of_genres():
    return [Genre("A"), Genre("D"), Genre("C"), Genre("B")]


# testing services for game_info
def test_game_info_retrieve_game(in_memory_repo):
    game = games_info_services.get_game_by_id(267360, in_memory_repo)
    assert game == Game(267360, "MURI")
    # tests game_info retrieves the correct game


def test_game_info_add_review(in_memory_repo):
    game_id = 7940
    rating = 5
    review_text = "Great game, would recommend!"
    user_name = "kevin"
    games_info_services.add_review(game_id, rating, review_text, user_name, in_memory_repo)
    game = games_info_services.get_game_by_id(game_id, in_memory_repo)
    assert str(game.reviews) == "[Review(User: <User kevin>, Game: <Game 7940, Call of Duty® 4: Modern Warfare®>, Rating: 5, Comment: Great game, would recommend!)]"
    # This tests if game_info services can add a valid review


def test_game_info_add_game_to_favourites(in_memory_repo):
    user_name = "kevin"
    game_id = 1581010
    games_info_services.add_game_to_favourites(game_id, user_name, in_memory_repo)
    user = games_info_services.get_user(user_name, in_memory_repo)
    assert "<Game 1581010, Haunted House - The Murder>" in str(user.favourite_games)
    # This tests if game_info services can add a valid game to a valid user's favourites list


def test_game_info_remove_game_from_favourites(in_memory_repo):
    user_name = "kevin"
    game_id = 7940
    games_info_services.remove_game_from_favourites(game_id, user_name, in_memory_repo)
    user = games_info_services.get_user(user_name, in_memory_repo)
    assert str(user.favourite_games) == "[<Game 1228870, Bartlow's Dread Machine>, <Game 311120, The Stalin Subway: Red Veil>]"
    # This tests if game_info services can remove a valid game from a valid user's favourites list


def test_game_info_get_user(in_memory_repo):
    user = games_info_services.get_user("kevin", in_memory_repo)
    assert str(user) == "<User kevin>"
    # This tests if game_info services can get a user from repo


# testing services for game_library
def test_game_library_retrieve_games_by_genre(in_memory_repo):
    games = games_library_services.get_games_by_genre("RPG", 1, 10, in_memory_repo)
    assert (str(sorted(games)[:3]) ==
            "[<Game 648510, Choice of the Star Captain>, <Game 656740, Cosmonator>, <Game 658970, CasinoRPG>]")
    # Tests game_library can retrieve games by genre correctly with a valid genre
    assert len(games) == 10
    # Tests pagination returns the correct number of pages
    assert len(games_library_services.get_games_by_genre(
        "Invalid", 1, 10, in_memory_repo)) == 0
    # Tests gets no games if invalid genre
    games_fourth_page = games_library_services.get_games_by_genre("RPG", 3, 3, in_memory_repo)
    assert (str(games_fourth_page) ==
            "[<Game 2011540, Blue Star Mobile Team>, <Game 926140, CHANGE: A Homeless Survival Experience>, <Game 658970, CasinoRPG>]")
    # Tests pagination returns the correct page of games


def test_game_library_retrieve_games_by_search(in_memory_repo):
    games = games_library_services.get_games_by_search("Title", "call of", 0, 10, in_memory_repo)
    assert str(sorted(games)) == "[<Game 7940, Call of Duty® 4: Modern Warfare®>]"
    assert len(games) == 1
    # Tests that game_library search function can search a title of a game
    games = games_library_services.get_games_by_search("Publisher", "act", 0, 3, in_memory_repo)
    assert (str(sorted(games)) ==
            "[<Game 376410, Acaratus>, <Game 461830, Adventure Apes and the Mayan Mystery>, "
            "<Game 532080, Apocalypse Mechanism>]")
    assert len(games) == 3
    # Tests that game_library search function can search for a publisher, and will return all games for the publisher
    games = games_library_services.get_games_by_search("Genre", "RpG", 3, 3, in_memory_repo)
    assert (str(sorted(games)) ==
            "[<Game 658970, CasinoRPG>, <Game 926140, CHANGE: A Homeless Survival Experience>, "
            "<Game 2011540, Blue Star Mobile Team>]")
    assert len(games) == 3
    # Tests that game_library search function can search for a genre, and will return all games for the genre


def test_game_library_get_genres(in_memory_repo):
    genres = games_library_services.get_genres(in_memory_repo)
    assert len(genres) == 24
    # Tests the number of genres is correct
    genres.sort()
    assert str(genres[:3]) == "[<Genre Action>, <Genre Adventure>, <Genre Animation & Modeling>]"
    # Tests the list of genres is correct, and correctly in alpha order


def test_game_library_get_num_of_games_in_search(in_memory_repo):
    assert games_library_services.get_num_of_games_in_search("Title", "", in_memory_repo) == 877
    # Tests there are 877 games and that "" general searches for all of them
    assert games_library_services.get_num_of_games_in_search("Title", "of", in_memory_repo) == 83
    # Tests there are 83 games that have "of" in their title
    assert games_library_services.get_num_of_games_in_search("Title", "Crazy Critters - Combat Cats", in_memory_repo) == 1
    # Tests there is only 1 game for a specific title
    assert games_library_services.get_num_of_games_in_search("Title", "crazy critters - combat cats", in_memory_repo) == 1
    # Tests that the search is not case-sensitive
    assert games_library_services.get_num_of_games_in_search("Genre", "action", in_memory_repo) == 380
    # Tests the total number of games in a genre search (action) is correct (380)
    assert games_library_services.get_num_of_games_in_search("Publisher", "act", in_memory_repo) == 31
    # Tests the total number of games with a publisher search for "act" in it is correct (31)
    assert games_library_services.get_num_of_games_in_search("Publisher", "activision", in_memory_repo) == 1
    # Tests the total number of games with a specific publisher name search (activision) is correct (1)


def test_game_library_get_num_of_games_in_genre(in_memory_repo):
    assert games_library_services.get_num_of_games_in_genre("RPG", in_memory_repo) == 131
    # Tests get number of games in genre works with getting the number of games in a whole genre
    assert games_library_services.get_num_of_games_in_genre("Invalid", in_memory_repo) == 0
    # Tests get number of games in genre will return 0 for a non-existing genre
    assert games_library_services.get_num_of_games_in_genre("Adventure", in_memory_repo) == 344
    # Tests get number of games in genre works with getting the number of games in a whole genre that's not just RPG


def test_game_library_get_last_page_num():
    assert games_library_services.get_last_page_num(3, 2) == 1
    assert games_library_services.get_last_page_num(3, 3) == 0
    assert games_library_services.get_last_page_num(4, 2) == 1
    # These test cases are all for last page calculation edge cases


def test_game_library_get_num_of_genres(in_memory_repo):
    assert games_library_services.get_num_of_genres(in_memory_repo) == 24
    # Tests get number of genres works in game_library


def test_game_library_alpha_sort_games(list_of_games):
    games_library_services.alpha_sort_games(list_of_games)
    assert str(list_of_games) == "[<Game 1, A>, <Game 2, B>, <Game 3, C>, <Game 4, D>]"
    # Tests game_library sorts games correctly


def test_game_library_alpha_sort_genres(list_of_genres):
    games_library_services.alpha_sort_genres(list_of_genres)
    assert str(list_of_genres) == "[<Genre A>, <Genre B>, <Genre C>, <Genre D>]"
    # Tests game_library sorts genres correctly


# testing services for user_info
def test_user_info_get_user(in_memory_repo):
    user = user_info_services.get_user("kevin", in_memory_repo)
    assert str(user) == "<User kevin>"
    # This tests if user_info services can get a user from repo


# testing services for authentication
def test_auth_add_user(in_memory_repo):
    user_name = 'jevin'
    password = 'abcd1A23'
    auth_services.add_user(user_name, password, in_memory_repo)
    user_dict = auth_services.get_user(user_name, in_memory_repo)
    assert user_dict['user_name'] == user_name

    # Check that password has been encrypted.
    assert user_dict['password'].startswith('pbkdf2:sha256:')
    # Tests auth adds a user correctly


def test_auth_add_user_with_same_name(in_memory_repo):
    user_name = 'kevin'
    password = 'abcd1A23'

    with pytest.raises(auth_services.NameNotUniqueException):
        auth_services.add_user(user_name, password, in_memory_repo)
    # Tests auth cannot add a user with the same username


def test_auth_with_valid_credentials(in_memory_repo):
    user_name = 'new_person'
    password = 'crazy123!'

    auth_services.add_user(user_name, password, in_memory_repo)

    try:
        auth_services.authenticate_user(user_name, password, in_memory_repo)
    except AuthenticationException:
        assert False
    # Tests authenticating a user with the right login works


def test_auth_with_invalid_credentials(in_memory_repo):
    user_name = 'new_person'
    password = 'crazy123!'

    auth_services.add_user(user_name, password, in_memory_repo)

    with pytest.raises(auth_services.AuthenticationException):
        auth_services.authenticate_user(user_name, 'incorrect_password', in_memory_repo)
    # Tests authenticating a user with the incorrect password will throw an error
