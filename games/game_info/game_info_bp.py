from flask import Blueprint, render_template

game_info_bp = Blueprint('game_info_bp', __name__)

@game_info_bp.route('/game_info')
def game_info():
    return render_template('game_info.html')
