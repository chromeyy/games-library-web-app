import abc

repo_instance = None

class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add_games(self, game):
        raise NotImplementedError

    @abc.abstractmethod
    def get_games_by_genre(self, genre_name):
        raise NotImplementedError

    def get_games_by_publisher(self, publisher_name):
        raise NotImplementedError

    def get_games_by_search(self, search_term):
        raise NotImplementedError

