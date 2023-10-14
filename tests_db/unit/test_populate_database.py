from sqlalchemy import select, inspect

from games import metadata

#add comments

def test_database_populate_inspect_table_names(database_engine):
    inspector = inspect(database_engine)
    assert inspector.get_table_names() == ['game_genres', 'users', 'games', 'reviews', 'genres']


def test_database_populate_select_all_users(database_engine):
    inspector = inspect(database_engine)
    name_of_users_table = inspector.get_table_names()[1]

    with database_engine.connect() as connection:
        # query for records in table users
        select_statement = select([metadata.tables[name_of_users_table]])
        result = connection.execute(select_statement)

        all_users = []
        for row in result:
            all_users.append(row['user_name'])

        assert all_users == ['kevin', 'tom']


def test_database_populate_select_all_genres(database_engine):
    # inspector = inspect(database_engine)
    # genres_table = inspector.get_table_names()[5]

    # with database_engine.connect() as connection:
        # select_statement = select([metadata.tables[genres_table]])
        # result = connection.execute(select_statement)

        # all_genres = []
        # for row in result:
        #    all_reviews.append((row['genre']))

        # nr_genres = len(all_genres)
        # assert nr_genres == 6 <--- fix this

        # assert all_reviews0] == <--- fix this
        pass


def test_database_populate_select_all_reviews(database_engine):
    # inspector = inspect(database_engine)
    # reviews_table = inspector.get_table_names()[3]

    # with database_engine.connect() as connection:
        # select_statement = select([metadata.tables[reviews_table]])
        # result = connection.execute(select_statement)

        # all_reviews = []
        # for row in result:
        #    all_reviews.append((row['user'], row['game'], row['rating'], row['comment']))

        # nr_reviews = len(all_reviews)
        # assert nr_reviews == 6 <--- fix this

        # assert all_reviews0] == <--- fix this
        pass


def test_database_populate_select_all_games(database_engine):
    # inspector = inspect(database_engine)
    # name_of_games_table = inspector.get_table_names()[2]

    # with database_engine.connect() as connection:
        # select_statement = select([metadata.tables[name_of_games_table]])
        # result = connection.execute(select_statement)

        # all_games = []
        # for row in result:
        #    all_games.append((row['id'], row['title']))

        # nr_games = len(all_games)
        # assert nr_games == 6 <--- fix this

        # assert all_games[0] == <--- fix this
        pass

