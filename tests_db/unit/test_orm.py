import pytest
import datetime
from sqlalchemy.exc import IntegrityError


# USER
def insert_user(empty_session, values=None):
    pass


def insert_users(empty_session, values):
    pass


def make_user():
    pass


def test_loading_users(empty_session):
    pass


def test_saving_users(empty_session):
    pass


# GENRE
def insert_genre(empty_session, values=None):
    pass


def insert_genres(empty_session, values):
    pass


def make_genre():
    pass


# REVIEW
def insert_review(empty_session, values=None):
    pass


def insert_reviews(empty_session, values):
    pass


def make_review():
    pass


def test_saving_review(empty_session):
    pass


def test_loading_review(empty_session):
    pass


# FAVOURITES
def insert_favourite(empty_session, values=None):
    pass


def insert_favourites(empty_session, values):
    pass


def make_favourite():
    pass


def test_saving_favourite(empty_session):
    pass


def test_loading_favourite(empty_session):
    pass


# GAME

def insert_game(empty_session, values=None):
    pass


def insert_games(empty_session, values):
    pass


def make_game():
    pass


def test_saving_game(empty_session):
    pass


def test_loading_game(empty_session):
    pass


def test_saving_game_with_genre(empty_session):
    pass

def test_loading_game_with_genre(empty_session):
    pass