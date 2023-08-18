from flask import Blueprint, render_template
from ..adapters.datareader.csvdatareader import GameFileCSVReader

game_library_bp = Blueprint('game_library_bp', __name__)

@game_library_bp.route('/game_library/<current_page>')
def game_library(current_page):

    current_page = int(current_page)
    items_per_page = 10

    #create instance of GameFileCSVReader
    file_reader = GameFileCSVReader("games/adapters/data/games.csv")
    #read csv file
    file_reader.read_csv_file()

    #store list of all game objects
    games_dataset = file_reader.dataset_of_games

    return render_template(
        'game_library.html',
        current_page=current_page,
        games_dataset=games_dataset[current_page * items_per_page:current_page * items_per_page + items_per_page]
        )
