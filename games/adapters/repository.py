import abc

repo_instance = None

class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add_user(self, user):
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, user_name):
        raise NotImplementedError

    @abc.abstractmethod
    def add_games(self, game):
        raise NotImplementedError

    @abc.abstractmethod
    def get_games_by_genre(self, genre_name):
        raise NotImplementedError

    @abc.abstractmethod
    def get_games_by_publisher(self, publisher_name):
        raise NotImplementedError

    @abc.abstractmethod
    def get_games_by_search(self, search_category, search_term):
        raise NotImplementedError

    @abc.abstractmethod
    def get_game_by_id(self, game_id):
        raise NotImplementedError

    @abc.abstractmethod
    def add_genre(self, genre):
        raise NotImplementedError

    @abc.abstractmethod
    def get_list_of_genres(self):
        raise NotImplementedError

    @abc.abstractmethod
    def add_review(self, review):
        raise NotImplementedError

    @abc.abstractmethod
    def get_reviews(self):
        raise NotImplementedError
