from flask import Blueprint, render_template
from ..adapters.datareader.csvdatareader import GameFileCSVReader

game_library_bp = Blueprint('game_library_bp', __name__)

@game_library_bp.route('/game_library')
def game_library():

    MAX_GAMES_PER_PAGE = 10

    #create instance of GameFileCSVReader
    file_reader = GameFileCSVReader("games/adapters/data/games.csv")
    #read csv file
    file_reader.read_csv_file()

    #store list of all game objects
    games_dataset = file_reader.dataset_of_games

    return render_template('game_library.html', games_dataset = games_dataset[:MAX_GAMES_PER_PAGE - 1])
