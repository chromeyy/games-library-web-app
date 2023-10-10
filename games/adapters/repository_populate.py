from games.adapters.repository import AbstractRepository
from pathlib import Path
from games.adapters.datareader.csvdatareader import GameFileCSVReader
from games.adapters.csv_data_importer import load_users, load_reviews, load_favourites


def populate(data_path, repo: AbstractRepository):
    filename = str(Path(data_path) / "games.csv")
    file_reader = GameFileCSVReader(filename)
    file_reader.read_csv_file()

    for game in file_reader.dataset_of_games:
        repo.add_games(game)

    for genre in file_reader.dataset_of_genres:
        repo.add_genre(genre)

    users = load_users(data_path, repo)

    load_reviews(data_path, repo, users)
    load_favourites(data_path, repo, users)
