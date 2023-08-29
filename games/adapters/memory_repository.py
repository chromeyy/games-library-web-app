import games.adapters.repository as abstract_repo
from pathlib import Path
from games.domainmodel.model import Game
from games.adapters.datareader.csvdatareader import GameFileCSVReader


class MemoryRepository(abstract_repo.AbstractRepository):
    def __init__(self):
        self.__games = list()
        self.__games_index = dict()

    def get_games_by_genre(self, selected_genre='all'):
        if selected_genre == 'all':
            games_dataset = self.__games.copy()
        else:
            games_dataset = list()
            for game in self.__games:
                for genre in game.genres:
                    if genre.genre_name == selected_genre:
                        games_dataset.append(game)
                        break
        return games_dataset

    def get_games_by_publisher(self, selected_publisher='all'):
        if selected_publisher == 'all':
            games_dataset = self.__games.copy()
        else:
            games_dataset = list()
            for game in self.__games:
                if game.publisher.publisher_name == selected_publisher:
                    games_dataset.append(game)
        return games_dataset

    def get_games_by_search(self, search_category='title', search_term=''):
        games_dataset = list()

        if search_term == '':
            games_dataset = self.__games.copy()

        elif search_category == 'Title':
            for game in self.__games:
                if search_term.lower() in game.title.lower():
                    games_dataset.append(game)

        elif search_category == 'Genre':
            for game in self.__games:
                for genre in game.genres:
                    if search_term.lower() in genre.genre_name.lower():
                        games_dataset.append(game)
                        break

        elif search_category == 'Publisher':
            for game in self.__games:
                if search_term.lower() in game.publisher.publisher_name.lower():
                    games_dataset.append(game)

        return games_dataset

    def add_games(self, game):
        if isinstance(game, Game):
            self.__games.append(game)
            self.__games_index[game.game_id] = game

    def get_game_by_id(self, game_id) -> Game:
        game = None

        try:
            game = self.__games_index[int(game_id)]
        except KeyError:
            pass
        return game

def populate(data_path, repo: MemoryRepository):
    filename = str(Path(data_path) / "games.csv")
    file_reader = GameFileCSVReader(filename)
    file_reader.read_csv_file()

    for game in file_reader.dataset_of_games:
        repo.add_games(game)