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
        pass

    def get_games_by_publisher(self, selected_publisher='all'):
        pass

    def get_games_by_search(self, search_category='title', search_term=''):
        pass

    def add_games(self, game):
        with self._session_cm as scm:
            scm.session.add(game)
            scm.commit()

    def get_game_by_id(self, game_id) -> Game:
        pass

    def add_genre(self, genre):
        with self._session_cm as scm:
            scm.session.add(genre)
            scm.commit()

    def get_list_of_genres(self):
        pass

    def add_user(self, user: User):
        with self._session_cm as scm:
            scm.session.add(user)
            scm.commit()

    def get_user(self, username) -> User:
        user = None
        try:
            user = self._session_cm.session.query(User).filter(User._User__user_name == username).one()
        except NoResultFound:
            # Ignore any exception and return None.
            pass

        return user

    def add_review(self, review: Review):
        with self._session_cm as scm:
            scm.session.add(review)
            scm.commit()

    def get_reviews(self):
        pass
