from flask import Blueprint, render_template, request, session
import games.user_info.services as services
import games.adapters.repository as repo

from games.authentication.authentication_bp import login_required

user_info_bp = Blueprint('user_info_bp', __name__)


@user_info_bp.route('/user_info')
@login_required
def user_info():
    username = session['user_name']
    user = services.get_user(username, repo.repo_instance)

    return render_template('user_info.html', user=user)
