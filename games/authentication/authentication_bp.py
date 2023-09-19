from flask import Blueprint

authentication_bp = Blueprint(
    'authentication_bp', __name__, url_prefix='/authentication')


@authentication_bp.route('/register')
def register():
    # implement
    pass


@authentication_bp.route('/register_success')
def register_success():
    # implement
    pass


@authentication_bp.route('/login')
def login():
    # implement
    pass


@authentication_bp.route('logout')
def logout():
    # implement
    pass
