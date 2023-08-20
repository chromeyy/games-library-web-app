from flask import Blueprint, render_template
from ..adapters.datareader.csvdatareader import GameFileCSVReader

game_library_bp = Blueprint('game_library_bp', __name__)

@game_library_bp.route('/game_library/<selected_genre>/<current_page>')
def game_library(selected_genre, current_page):

    current_page = int(current_page)
    items_per_page = 10

    #create instance of GameFileCSVReader
    file_reader = GameFileCSVReader("games/adapters/data/games.csv")
    #read csv file
    file_reader.read_csv_file()

    if selected_genre == '_':
        games_dataset = file_reader.dataset_of_games
    else:
        games_dataset = []
        for game in file_reader.dataset_of_games:
            for genre in game.genres:
                if genre.genre_name == selected_genre:
                    games_dataset.append(game)
                    break

    return render_template(
        'game_library.html',
        selected_genre=selected_genre,
        current_page=current_page,
        games_dataset=games_dataset[current_page * items_per_page:current_page * items_per_page + items_per_page]
        )

