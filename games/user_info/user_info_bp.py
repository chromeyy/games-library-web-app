from flask import Blueprint, render_template, request
import games.user_info.services as services
import games.adapters.repository as repo

user_info_bp = Blueprint(
    'user_info_bp', __name__)


@user_info_bp.route('/user_info')
def user_info():
    username = request.args.get('username')
    user = services.get_user(username, repo.repo_instance)

    return render_template('user_info.html', user=user)
