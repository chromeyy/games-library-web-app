from sqlalchemy import desc, asc
from sqlalchemy.orm.exc import NoResultFound

from sqlalchemy.orm import scoped_session

import games.adapters.repository as abstract_repo
from games.domainmodel.model import Game, Genre, User, Review


class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        # this method can be used e.g. to allow Flask to start a new session for each http request,
        # via the 'before_request' callback
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory)

    def close_current_session(self):
        if self.__session is not None:
            self.__session.close()


class SqlAlchemyRepository(abstract_repo.AbstractRepository):
    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()

    def get_games_by_genre(self, selected_genre='all'):
        if selected_genre == 'all':
            # If selected all genres return all games
            return self._session_cm.session.query(Game).all()
        else:
            games = []
            # Select games by a genre
            # Get game ids from games genres table that are related to the selected genre
            game_ids = self._session_cm.session.execute('SELECT game_id FROM game_genres WHERE genre_name = :selected_genre', {'selected_genre': selected_genre}).fetchall()
            if not game_ids:
                return games
            game_ids = [game_id[0] for game_id in game_ids]

            # Query all games that match those ids
            games = self._session_cm.session.query(Game).filter(Game._Game__game_id.in_(game_ids)).all()

            return games

    def get_games_by_publisher(self, selected_publisher='all'):
        pass

    def get_games_by_search(self, search_category='title', search_term=''):
        games = list()

        def get_games_by_fetched_ids(ids):
            if not ids:
                return []
            ids = [game_id[0] for game_id in ids]
            return self._session_cm.session.query(Game).filter(Game._Game__game_id.in_(ids)).all()

        if search_term == '':
            return self._session_cm.session.query(Game).all()

        elif search_category == 'Title':
            search_title = '%' + search_term + '%'
            game_ids = self._session_cm.session.execute('SELECT game_id FROM games WHERE genre_name LIKE search_title',
                                                        {'search_title': search_title}).fetchall()
            games = get_games_by_fetched_ids(game_ids)

        elif search_category == 'Genre':
            search_genre = '%' + search_term + '%'
            game_ids = self._session_cm.session.execute('SELECT game_id FROM game_genres WHERE genre_name LIKE :search_genre',
                                                        {'search_genre': search_genre}).fetchall()
            games = get_games_by_fetched_ids(game_ids)

        elif search_category == 'Publisher':
            search_publisher = '%' + search_term + '%'
            game_ids = self._session_cm.session.execute('SELECT game_id FROM games WHERE publisher_name LIKE :search_publisher',
                                                        {'search_publisher': search_publisher}).fetchall()
            games = get_games_by_fetched_ids(game_ids)

        return games

    def add_games(self, game):
        with self._session_cm as scm:
            scm.session.merge(game)
            scm.commit()

    def get_game_by_id(self, game_id) -> Game:
        game = self._session_cm.session.query(Game).filter(Game._Game__game_id == game_id).one()
        return game

    def add_genre(self, genre):
        with self._session_cm as scm:
            scm.session.merge(genre)
            scm.commit()

    def get_list_of_genres(self):
        return self._session_cm.session.query(Genre).all()

    def add_user(self, user: User):
        with self._session_cm as scm:
            scm.session.add(user)
            scm.commit()

    def get_user(self, username) -> User:
        user = None
        try:
            user = self._session_cm.session.query(User).filter(User._User__username == username).one()
        except NoResultFound:
            # Ignore any exception and return None.
            pass

        return user

    def add_review(self, review: Review):
        with self._session_cm as scm:
            scm.session.merge(review)
            scm.commit()

    def get_reviews(self):
        pass
