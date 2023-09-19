import csv
import games.adapters.repository as abstract_repo
from pathlib import Path
from datetime import date, datetime
from games.domainmodel.model import Game, Genre, User, Review
from games.adapters.datareader.csvdatareader import GameFileCSVReader

class MemoryRepository(abstract_repo.AbstractRepository):
    def __init__(self):
        self.__games = list()
        self.__games_index = dict()
        self.__genres = list()
        self.__users = list()
        self.__reviews = list()

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

    def add_genre(self, genre):
        if isinstance(genre, Genre):
            self.__genres.append(genre)

    def get_list_of_genres(self):
        return self.__genres

    def add_user(self, user: User):
        self.__users.append(user)

    def get_user(self, user_name) -> User:
        pass
        # implementation of get_user
        # CWA implementation below
        # return next((user for user in self.__users if user.user_name == user_name), None)

    def add_review(self, review: Review):
        # call parent class first, add_comment relies on implementation of code common to all derived classes
        self.__reviews.append(review)

    def get_comments(self):
        return self.__reviews

def populate(data_path, repo: MemoryRepository):
    filename = str(Path(data_path) / "games.csv")
    file_reader = GameFileCSVReader(filename)
    file_reader.read_csv_file()

    for game in file_reader.dataset_of_games:
        repo.add_games(game)

    for genre in file_reader.dataset_of_genres:
        repo.add_genre(genre)

