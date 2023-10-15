from sqlalchemy import select, inspect

from games import metadata
from games.domainmodel.model import Review, Game, User, Genre


def test_database_populate_inspect_table_names(database_engine):
    inspector = inspect(database_engine)
    assert (inspector.get_table_names() == ['favourites', 'game_genres', 'games',
                                            'genres', 'publishers', 'reviews','users'])


def test_database_populate_select_all_users(database_engine):
    inspector = inspect(database_engine)
    name_of_users_table = inspector.get_table_names()[6]

    with database_engine.connect() as connection:
        select_statement = select([metadata.tables[name_of_users_table]])
        result = connection.execute(select_statement)

        all_users = []
        for row in result:
            all_users.append(row['username'])

        assert all_users == ['kevin', 'tom', 'tori']


def test_database_populate_select_all_genres(database_engine):
    inspector = inspect(database_engine)
    genres_table = inspector.get_table_names()[3]

    with database_engine.connect() as connection:
        select_statement = select([metadata.tables[genres_table]])
        result = connection.execute(select_statement)


        all_genres = []
        for row in result:
            all_genres.append((row['genre_name']))

        nr_genres = len(all_genres)
        assert nr_genres == 24
        assert all_genres[0] == 'Action'



def test_database_populate_select_all_reviews(database_engine):
    inspector = inspect(database_engine)
    reviews_table = inspector.get_table_names()[5]

    with database_engine.connect() as connection:
        select_statement = select([metadata.tables[reviews_table]])
        result = connection.execute(select_statement)

        all_reviews = []
        for row in result:
            all_reviews.append((row['review_text']))

        nr_reviews = len(all_reviews)
        assert nr_reviews == 3

        assert all_reviews[0] == 'Super cool'


def test_database_populate_select_all_games(database_engine):
    inspector = inspect(database_engine)
    name_of_games_table = inspector.get_table_names()[2]

    with database_engine.connect() as connection:
        select_statement = select([metadata.tables[name_of_games_table]])
        result = connection.execute(select_statement)

        all_games = []
        for row in result:
           all_games.append(row['game_title'])

        nr_games = len(all_games)
        assert nr_games == 877

        assert all_games[0] == 'Xpand Rally'

