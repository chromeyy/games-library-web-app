import pytest

from pathlib import Path
from games.domainmodel.model import *
import games.adapters.repository as repo
from games.adapters.memory_repository import MemoryRepository, populate

@pytest.fixture()
def game():
    return Game(123, "New Game")

def test_add_game(in_memory_repo, game):
    # Test repository can add a game object
    in_memory_repo.add_games(game)
    assert in_memory_repo.get_game_by_id("123") is game


def test_retrieve_game(in_memory_repo):
    # Test repository can retrieve a game object
    game = in_memory_repo.get_game_by_id(267360)
    assert game == Game(267360, "MURI")

# Test repository retrieves correct number of game objects

# Test the number of unique genres in the dataset
# Test repository adds a new genre, and the count of genres increases by 1.
# Test repository search games by title or publisher etc
# Test repository search games by genre name
