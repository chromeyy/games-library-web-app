import games.adapters.repository as abstract_repo
from pathlib import Path
from games.domainmodel.model import Game
from games.adapters.datareader.csvdatareader import GameFileCSVReader

class MemoryRepository(abstract_repo.AbstractRepository):
    def __init__(self):
        self.__games = list()

    def get_games(self, selected_genre='all', selected_publisher='all'):
        if selected_genre == 'all':
            games_dataset = self.__games.copy()
        else:
            games_dataset = list()
            for game in self.__games:
                for genre in game.genres:
                    if genre.genre_name == selected_genre:
                        games_dataset.append(game)
                        break

        if selected_publisher == 'all':
            pass
        else:
            new_dataset = []
            for game in games_dataset:
                if game.publisher.publisher_name == selected_publisher:
                    new_dataset.append(game)
            games_dataset = new_dataset

        return games_dataset

    def add_games(self, game):
        if isinstance(game, Game):
            self.__games.append(game)

def populate(data_path, repo: MemoryRepository):
    filename = str(Path(data_path) / "games.csv")
    file_reader = GameFileCSVReader(filename)
    file_reader.read_csv_file()

    for game in file_reader.dataset_of_games:
        repo.add_games(game)