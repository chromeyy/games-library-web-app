import pytest
import datetime
from sqlalchemy.exc import IntegrityError

from games.domainmodel.model import User, Genre, Review, Game


# USER
def insert_user(empty_session, values=None):
    new_name = "testuser"
    new_password = "test123"

    if values is not None:
        new_name = values[0]
        new_password = values[1]

    empty_session.execute('INSERT INTO users (user_name, password) VALUES (:user_name, :password)',
                          {'user_name': new_name, 'password': new_password})
    row = empty_session.execute('SELECT id from users where user_name = :user_name',
                                {'user_name': new_name}).fetchone()
    return row[0]

def insert_users(empty_session, values):
    for value in values:
        empty_session.execute('INSERT INTO users (user_name, password) VALUES (:user_name, :password)',
                              {'user_name': value[0], 'password': value[1]})
    rows = list(empty_session.execute('SELECT id from users'))
    keys = tuple(row[0] for row in rows)
    return keys


def make_user():
    user = User("test_user", "12345")
    return user


def test_loading_users(empty_session):
    users = list()
    users.append(("test_user_1", "test1234"))
    users.append(("test_user_2", "test54321"))
    insert_users(empty_session, users)

    expected = [
        User("test_user_1", "test1234"),
        User("test_user_2", "test54321")
    ]
    assert empty_session.query(User).all() == expected


def test_saving_users(empty_session):
    user = make_user()
    empty_session.add(user)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT user_name, password FROM users'))
    assert rows == [("test_user", "test1234")]


# GENRE
def insert_genre(empty_session, values=None):
    pass


def insert_genres(empty_session, values):
    pass


def make_genre():
    genre = Genre("test_genre")
    return genre


# REVIEW
def insert_review(empty_session, values=None):
    pass


def insert_reviews(empty_session, values):
    pass


def make_review():
    test_user = User('test', 'test_password')
    test_game = Game(100010001, 'test')
    review = Review(test_user, test_game, 1, "test_comment")
    return review


def test_saving_review(empty_session):
    pass


def test_loading_review(empty_session):
    pass


# FAVOURITES
def insert_favourite(empty_session, values=None):
    pass


def insert_favourites(empty_session, values):
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
    game = Game(100196, 'test_game')
    return game


def test_saving_game(empty_session):
    pass


def test_loading_game(empty_session):
    pass


def test_saving_game_with_genre(empty_session):
    pass

def test_loading_game_with_genre(empty_session):
    pass