import pytest

from pathlib import Path
from games.domainmodel.model import *
import games.adapters.repository as repo
from games.adapters.memory_repository import MemoryRepository, populate


@pytest.fixture()
def game():
    return Game(123, "New Game")


@pytest.fixture()
def genre():
    return Genre("New Testing Genre")


def test_add_game(in_memory_repo, game):
    # Test repository can add a game object
    in_memory_repo.add_games(game)
    assert in_memory_repo.get_game_by_id("123") is game


def test_retrieve_game_by_id(in_memory_repo):
    # Test repository can retrieve a game object
    game = in_memory_repo.get_game_by_id(267360)
    assert game == Game(267360, "MURI")


def test_cannot_retrieve_non_existent_game_id(in_memory_repo):
    game = in_memory_repo.get_game_by_id(6824305685601513678415)
    assert game is None


def test_add_genre(in_memory_repo, genre):
    previous_list_of_genres = in_memory_repo.get_list_of_genres().copy()
    in_memory_repo.add_genre(genre)
    assert genre in in_memory_repo.get_list_of_genres()
    assert genre not in previous_list_of_genres
    assert len(in_memory_repo.get_list_of_genres()) == len(previous_list_of_genres) + 1


def test_get_list_of_genres(in_memory_repo):
    list_of_genres = in_memory_repo.get_list_of_genres().copy()
    assert len(list_of_genres) == 24
    assert len(list_of_genres) == len(set(list_of_genres))
    assert str(sorted(list_of_genres)[:3]) == "[<Genre Action>, <Genre Adventure>, <Genre Animation & Modeling>]"


def test_retrieve_games_by_search(in_memory_repo):
    assert str(sorted(in_memory_repo.get_games_by_search('Title', "aLl"))[:3]) == "[<Game 3010, Xpand Rally>, <Game 7940, Call of Duty® 4: Modern Warfare®>, <Game 231330, Deadfall Adventures>]"
    assert str(sorted(in_memory_repo.get_games_by_search('Genre', "aC"))[:3]) == "[<Game 3010, Xpand Rally>, <Game 7940, Call of Duty® 4: Modern Warfare®>, <Game 12140, Max Payne>]"
    assert str(sorted(in_memory_repo.get_games_by_search('Publisher', "aCt"))[:3]) == "[<Game 7940, Call of Duty® 4: Modern Warfare®>, <Game 42920, The Kings' Crusade>, <Game 291690, Empathy: Path of Whispers>]"


def test_retrieve_game_by_genre(in_memory_repo):
    print(str(sorted(in_memory_repo.get_games_by_genre("RPG"))[:3]))
    assert str(sorted(in_memory_repo.get_games_by_genre("RPG"))[:3]) == "[<Game 65600, Gothic 3: Forsaken Gods Enhanced Edition>, <Game 201010, Geneforge 5: Overthrow>, <Game 226620, Desktop Dungeons>]"
