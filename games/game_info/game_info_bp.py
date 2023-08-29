from flask import Blueprint, render_template, request

game_info_bp = Blueprint('game_info_bp', __name__)

@game_info_bp.route('/game_info')
def game_info():

    game_id = request.args.get('game_id')


    return render_template('game_info.html', game_id=game_id)
