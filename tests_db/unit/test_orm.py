import pytest
import datetime
from sqlalchemy.exc import IntegrityError

from games.domainmodel.model import User, Genre, Review, Game, Publisher


# USER
def insert_user(current_session, values=None):
    new_name = "testuser"
    new_password = "test123"

    if values is not None:
        new_name = values[0]
        new_password = values[1]

    current_session.execute('INSERT INTO users (username, password) VALUES (:username, :password)',
                            {'username': new_name, 'password': new_password})
    row = current_session.execute('SELECT user_id from users where username = :username',
                                  {'username': new_name}).fetchone()
    return row[0]


def test_loading_users(empty_session):
    users = list()
    users.append(("test_user_1", "test1234"))
    users.append(("test_user_2", "test54321"))
    insert_user(empty_session, users[0])
    insert_user(empty_session, users[1])

    expected = [
        User("test_user_1", "test1234"),
        User("test_user_2", "test54321")
    ]
    assert empty_session.query(User).all() == expected


def test_saving_users(empty_session):
    user = User("test_user_1", "@Test123")
    empty_session.add(user)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT username, password FROM users'))
    assert rows == [("test_user_1", "@Test123")]


# GENRE
def insert_genre(empty_session, value=None):
    new_genre = "test_genre"

    if value is not None:
        new_genre = value

    empty_session.execute('INSERT INTO genres (genre_name) VALUES (:genre_name)',
                          {'genre_name': new_genre})
    row = empty_session.execute('SELECT genre_name from genres where genre_name = :genre_name',
                                {'genre_name': new_genre}).fetchone()
    return row[0]


def test_saving_genre(empty_session):
    genre = Genre("test_genre")
    empty_session.add(genre)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT genre_name FROM genres'))
    assert rows == [("test_genre",)]


def test_loading_genre(empty_session):  # keeps failing
    genres = list()
    genres.append("test_genre")
    genres.append("test_genre_2")

    insert_genre(empty_session, genres[0])
    insert_genre(empty_session, genres[1])
    expected = [
        Genre("test_genre"),
        Genre("test_genre_2")
    ]
    assert empty_session.query(Genre).all() == expected


# REVIEW
def insert_review(current_session, values=None):
    new_user = 80085
    new_game_id = 80085
    new_rating = 5
    new_comment = "great!"

    if values is not None:
        new_user = values[0]
        new_game_id = values[1].game_id
        new_rating = values[2]
        new_comment = values[3]

    user_id = current_session.execute('SELECT user_id FROM users WHERE username LIKE :username',
                                      {'username': new_user.username}).fetchone()

    current_session.execute('INSERT INTO reviews (game_id, user_id, review_text, rating) VALUES '
                            '(:game_id, :user_id, :review_text, :rating)',
                            {'game_id': new_game_id, 'user_id': user_id[0], 'review_text': new_comment,
                             'rating': new_rating})
    row = current_session.execute('SELECT rating FROM reviews Where review_text = :review_text',
                                  {'review_text': new_comment}).fetchone()
    return row[0]


def test_saving_review(empty_session):
    user = User('test1', 'Test1234@')
    game = Game(80085, 'test_game')
    game.release_date = "Oct 18, 2003"
    game.price = float(5)
    game.description = "test desc"
    game.image_url = "url"
    publisher = Publisher("testPub")
    game.publisher = publisher
    genre = Genre("testGenre")
    game.add_genre(genre)
    test_review = Review(user, game, 5, "test_review")
    empty_session.add(test_review)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT game_id, review_text FROM reviews'))
    assert rows == [(game.game_id, "test_review",)]


def test_loading_review(empty_session):
    reviews = list()
    game = Game(80086, 'test_game')
    game.release_date = "Oct 18, 2003"
    game.price = float(5)
    game.description = "test desc"
    game.image_url = "url"
    publisher = Publisher("testPub")
    game.publisher = publisher
    game.add_genre(Genre('test_genre'))

    user = User("potatoman", "Potato#1234")
    user2 = User("totatoman", "Totato#1234")

    insert_user(empty_session, ("potatoman", "Potato#1234"))
    insert_user(empty_session, ("totatoman", "Totato#1234"))

    insert_game(empty_session)

    insert_review(empty_session, (user, game, 5, "great!"))  # adding a new review
    insert_review(empty_session, (user2, game, 3, "not so amazing"))  # adding a second new review

    expected = [
        Review(user, game, 5, "great!"),
        Review(user2, game, 3, "not so amazing")
    ]
    assert empty_session.query(Review).all() == expected


# FAVOURITES
def test_saving_favourite(empty_session):
    user = User('test1', 'Test1234@')
    game = Game(80085, 'test_game')
    game.release_date = "Oct 18, 2003"
    game.price = float(5)
    game.description = "test desc"
    game.image_url = "url"
    publisher = Publisher("testPub")
    game.publisher = publisher
    genre = Genre("testGenre")
    game.add_genre(genre)
    user.add_favourite_game(game)
    empty_session.add(user)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT game_id FROM favourites'))
    assert rows == [(game.game_id,)]


def insert_favourite(current_session, values=None):
    new_user = 80085
    new_game_id = 80085

    if values is not None:
        new_user = values[0]
        new_game_id = values[1].game_id

    user_id = current_session.execute('SELECT user_id FROM users WHERE username LIKE :username',
                                      {'username': new_user.username}).fetchone()

    current_session.execute('INSERT INTO favourites (game_id, user_id) VALUES '
                            '(:game_id, :user_id)',
                            {'game_id': new_game_id, 'user_id': user_id[0]})
    row = current_session.execute('SELECT game_id FROM favourites Where user_id = :user_id',
                                  {'user_id': user_id[0]}).fetchall()
    row = [item[0] for item in row]
    return row


def test_loading_favourite(empty_session):
    favourites = list()
    game = Game(80086, 'test_game')
    game.release_date = "Oct 18, 2003"
    game.price = float(5)
    game.description = "test desc"
    game.image_url = "url"
    publisher = Publisher("testPub")
    game.publisher = publisher
    game.add_genre(Genre('test_genre'))

    game2 = Game(80087, 'test_game2')
    game2.release_date = "Oct 18, 2003"
    game2.price = float(5)
    game2.description = "test desc"
    game2.image_url = "url"
    publisher = Publisher("testPub")
    game2.publisher = publisher
    game2.add_genre(Genre('test_genre'))

    user = User("potatoman", "Potato#1234")

    user_id = insert_user(empty_session, ("potatoman", "Potato#1234"))

    insert_game(empty_session)
    insert_game(empty_session, (game2.game_id, game2.title, game2.release_date,
                                game2.price, game2.description, game2.image_url, game2.publisher.publisher_name))

    insert_favourite(empty_session, (user, game))  # adding a new favourite
    insert_favourite(empty_session, (user, game2))  # adding a second new favourite

    game_ids = empty_session.execute('SELECT game_id FROM favourites WHERE user_id = :user_id',
                                               {'user_id': user_id}).fetchall()
    game_ids = [item[0] for item in game_ids]
    print(game_ids)

    expected = [game, game2]

    assert empty_session.query(Game).filter(Game._Game__game_id.in_(game_ids)).all() == expected


# GAME

def insert_game(current_session, values=None):
    game_id = 80086
    game_title = "test_game"
    release_date = "Oct 18, 2003"
    price = float(5)
    description = "test desc"
    image_url = "url"
    publisher = "testPub"

    if values is not None:
        game_id = values[0]
        game_title = values[1]
        release_date = values[2]
        price = values[3]
        description = values[4]
        image_url = values[5]
        publisher = values[6]

    current_session.execute('INSERT INTO games (game_id, game_title, game_price, release_date, '
                            'game_description, game_image_url, publisher_name) '
                            'VALUES (:game_id, :game_title, :game_price, :release_date, '
                            ':game_description, :game_image_url, :publisher_name)',
                            {'game_id': game_id, 'game_title': game_title, 'game_price': price,
                             'release_date': release_date,
                             'game_description': description, 'game_image_url': image_url, 'publisher_name': publisher})
    row = current_session.execute('SELECT game_title from games where game_title = :game_title',
                                  {'game_title': game_title}).fetchone()
    return row[0]


def insert_game_with_genre(current_session, values=None):
    game_id = 80086
    game_title = "test_game"
    release_date = "Oct 18, 2003"
    price = float(5)
    description = "test desc"
    image_url = "url"
    publisher = "testPub"
    genre_name = "genre"

    if values is not None:
        game_id = values[0]
        game_title = values[1]
        release_date = values[2]
        price = values[3]
        description = values[4]
        image_url = values[5]
        publisher = values[6]
        genre_name = values[7]

    current_session.execute('INSERT INTO games (game_id, game_title, game_price, release_date, '
                            'game_description, game_image_url, publisher_name) '
                            'VALUES (:game_id, :game_title, :game_price, :release_date, '
                            ':game_description, :game_image_url, :publisher_name)',
                            {'game_id': game_id, 'game_title': game_title, 'game_price': price,
                             'release_date': release_date,
                             'game_description': description, 'game_image_url': image_url, 'publisher_name': publisher})

    current_session.execute('INSERT INTO game_genres (game_id, genre_name) VALUES (:game_id, :genre_name)',
                            {'game_id': game_id, 'genre_name': genre_name})

    row = current_session.execute('SELECT game_id from game_genres where genre_name = :genre_name',
                                  {'genre_name': genre_name}).fetchone()
    return row[0]


def test_saving_game(empty_session):
    new_title = 'test_game'
    new_id = 80085
    game = Game(new_id, new_title)
    game.release_date = "Oct 18, 2003"
    game.price = float(5)
    game.description = "test desc"
    game.image_url = "url"
    publisher = Publisher("testPub")
    game.publisher = publisher

    empty_session.add(game)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT game_id, game_title FROM games'))
    assert rows == [(new_id, new_title,)]


def test_loading_game(empty_session):
    game_id = 80086
    game_title = "test_game"
    release_date = "Oct 18, 2003"
    price = float(5)
    description = "test desc"
    image_url = "url"
    publisher = "testPub"

    game = Game(game_id, game_title)
    game.price = price
    game.release_date = release_date
    game.description = description
    game.image_url = image_url
    game.publisher = Publisher(publisher)

    insert_game(empty_session, (game_id, game_title, release_date, price, description, image_url, publisher))
    expected = [game]
    assert empty_session.query(Game).all() == expected


def test_saving_game_with_genre(empty_session):
    new_title = 'test_game'
    new_id = 80085
    game = Game(new_id, new_title)
    game.release_date = "Oct 18, 2003"
    game.price = float(5)
    game.description = "test desc"
    game.image_url = "url"
    publisher = Publisher("testPub")
    game.publisher = publisher
    genre = Genre("testGenre")
    game.add_genre(genre)

    empty_session.add(game)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT game_id, genre_name FROM game_genres'))
    assert rows == [(new_id, "testGenre",)]


def test_loading_game_with_genre(empty_session):
    game_id = 80086
    game_title = "test_game"
    release_date = "Oct 18, 2003"
    price = float(5)
    description = "test desc"
    image_url = "url"
    publisher = "testPub"
    genre_name = 'genre'

    game = Game(game_id, game_title)
    game.price = price
    game.release_date = release_date
    game.description = description
    game.image_url = image_url
    game.publisher = Publisher(publisher)
    game.add_genre(Genre(genre_name))

    insert_game_with_genre(empty_session,(game_id, game_title, release_date, price, description, image_url, publisher, genre_name))

    expected = [game]
    assert empty_session.query(Game).all() == expected
