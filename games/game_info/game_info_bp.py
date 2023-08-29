from flask import Blueprint, render_template, request
import games.game_info.services as services

game_info_bp = Blueprint('game_info_bp', __name__)

@game_info_bp.route('/game_info')
def game_info():

    game_id = request.args.get('game_id')
    game = services.get_game_by_id(game_id)

    return render_template('game_info.html', game=game)

