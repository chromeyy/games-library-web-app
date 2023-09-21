from flask import Blueprint, render_template, request
import games.game_info.services as services
import games.adapters.repository as repo

from games.authentication.authentication_bp import login_required

game_info_bp = Blueprint('game_info_bp', __name__)


@game_info_bp.route('/game_info')
def game_info():

    game_id = request.args.get('game_id')
    game = services.get_game_by_id(game_id, repo.repo_instance)

    return render_template('game_view/game_info.html', game=game)

@game_info_bp.route('/game_info/review_game')
@login_required
def review_game():
    game_id = request.args.get('game_id')
    game = services.get_game_by_id(game_id, repo.repo_instance)

    return render_template('game_view/review.html', game=game)
