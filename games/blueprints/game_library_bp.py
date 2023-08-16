from flask import Blueprint, render_template

game_library_bp = Blueprint('game_library_bp', __name__)

@game_library_bp.route('/game_library')
def game_library():
    return render_template('game_library.html')
