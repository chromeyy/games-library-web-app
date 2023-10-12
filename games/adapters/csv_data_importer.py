import csv
from games.adapters.repository import AbstractRepository
from pathlib import Path
from games.domainmodel.model import User, Review
from werkzeug.security import generate_password_hash


def read_csv_file(filename: str):
    with open(filename, encoding='utf-8-sig') as infile:
        reader = csv.reader(infile)

        headers = next(reader)

        for row in reader:
            row = [item.strip() for item in row]
            yield row


def load_users(data_path: Path, repo: AbstractRepository):
    users_map = dict()

    users = list()
    users_filename = str(Path(data_path) / "users.csv")
    for data_row in read_csv_file(users_filename):
        user = User(
            username=data_row[1],
            password=generate_password_hash(data_row[2])
        )
        users.append(user)
        users_map[data_row[0]] = user

    favourites_filename = str(Path(data_path) / "favourites.csv")
    for data_row in read_csv_file(favourites_filename):
        username = users_map[data_row[1]].username
        user = next((user for user in users if user.username == username), None)
        user.add_favourite_game(repo.get_game_by_id(data_row[2]))

    for user in users:
        repo.add_user(user)

    return users_map


def load_reviews(data_path: Path, repo: AbstractRepository, users):
    reviews_filename = str(Path(data_path) / "reviews.csv")
    for data_row in read_csv_file(reviews_filename):
        review = Review(
            users[data_row[1]],
            repo.get_game_by_id(data_row[2]),
            int(data_row[3]),
            data_row[4]
        )
        repo.add_review(review)
