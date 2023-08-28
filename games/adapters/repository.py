import abc

repo_instance = None

class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add_games(self, game):
        raise NotImplementedError

    @abc.abstractmethod
    def get_games(self, games_list):
        raise NotImplementedError

