import pytest

from games.domainmodel.model import *

from games.game_info import services as games_info_services
from games.game_library import services as games_library_services


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


# testing services for game_library
def test_game_library_retrieve_game_by_genre(in_memory_repo):
    games = games_library_services.get_games_by_genre("RPG", 1, 10, in_memory_repo)
    assert (str(sorted(games)[:3]) ==
            "[<Game 648510, Choice of the Star Captain>, <Game 656740, Cosmonator>, <Game 658970, CasinoRPG>]")
    assert len(games) == 10
    assert len(games_library_services.get_games_by_genre(
        "Invalid", 1, 10, in_memory_repo)) == 0
    games_second_page = games_library_services.get_games_by_genre("RPG", 3, 3, in_memory_repo)
    assert (str(games_second_page) ==
            "[<Game 2011540, Blue Star Mobile Team>, <Game 926140, CHANGE: A Homeless Survival Experience>, <Game 658970, CasinoRPG>]")


def test_game_library_retrieve_game_by_search(in_memory_repo):
    pass


def test_game_library_get_genres(in_memory_repo):
    pass


def test_game_library_get_num_of_games_in_search(in_memory_repo):
    assert games_library_services.get_num_of_games_in_search("Title", "", in_memory_repo) == 0
    assert games_library_services.get_num_of_games_in_search("Genre", "", in_memory_repo) == 0
    assert games_library_services.get_num_of_games_in_search("Genre", "", in_memory_repo) == 0


def test_game_library_get_num_of_games_in_genre(in_memory_repo):
    assert games_library_services.get_num_of_games_in_genre("RPG", in_memory_repo) == 131
    assert games_library_services.get_num_of_games_in_genre("Invalid", in_memory_repo) == 0
    assert games_library_services.get_num_of_games_in_genre("Adventure", in_memory_repo) == 344


def test_game_library_get_last_page_num():
    assert games_library_services.get_last_page_num(3, 2) == 2
    assert games_library_services.get_last_page_num(3, 3) == 1
    assert games_library_services.get_last_page_num(4, 2) == 2


def test_game_library_get_num_of_genres(in_memory_repo):
    assert games_library_services.get_num_of_genres(in_memory_repo) == 24


def test_game_library_alpha_sort_games(list_of_games):
    games_library_services.alpha_sort_games(list_of_games)
    assert str(list_of_games) == "[<Game 1, A>, <Game 2, B>, <Game 3, C>, <Game 4, D>]"


def test_game_library_alpha_sort_genres(list_of_genres):
    games_library_services.alpha_sort_genres(list_of_genres)
    assert str(list_of_genres) == "[<Genre A>, <Genre B>, <Genre C>, <Genre D>]"


# Test inserting non-existing search key throws exception
