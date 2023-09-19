from flask import Blueprint

user_info_bp = Blueprint(
    'user_info_bp', __name__)


@user_info_bp.route('/user_info')
def user_info():
    # implement
    pass
