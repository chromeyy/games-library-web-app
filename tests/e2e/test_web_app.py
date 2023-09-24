import pytest

from flask import session


def test_register(client):
    # Check that we retrieve the register page.
    response_code = client.get('/authentication/register').status_code
    assert response_code == 200

    # Check that we can register a user successfully, supplying a valid username and password.
    response = client.post(
        '/authentication/register',
        data={'user_name': 'gmichael', 'password': '@Vrya365'}
    )
    # check the user is redirected to the register success page.
    assert response.headers['Location'] == '/authentication/register_success'


@pytest.mark.parametrize(('user_name', 'password', 'message'), (
        ('', '', b'Your user name is required'),
        ('cj', '', b'Your user name is too short'),
        ('test', '', b'Your password is required'),
        ('test', 'test', b'Your password must be at least 8 characters, and contain an upper case letter,\
            a lower case letter and a digit'),
        ('tori', 'Test#6^0', b'Your user name is already taken - please supply another'),
))
def test_register_with_invalid_input(client, user_name, password, message):
    # check correct error message is displayed for a range of invalid register inputs
    response = client.post(
        '/authentication/register',
        data={'user_name': user_name, 'password': password}
    )
    assert message in response.data


def test_login(client, auth):
    # Check that we can retrieve the login page.
    status_code = client.get('/authentication/login').status_code
    assert status_code == 200

    # Check that a successful login generates a redirect to the homepage.
    response = auth.login()
    assert response.headers['Location'] == '/'

    # Check that a session has been created for the logged-in user.
    with client:
        client.get('/')
        assert session['user_name'] == 'kevin'


def test_logout(client, auth):
    auth.login()

    # Check user session no longer exists
    with client:
        auth.logout()
        assert 'user_id' not in session


def test_index(client):
    # check that we can retrieve the index page
    response = client.get('/')
    assert response.status_code == 200


def test_login_required_to_review(client):
    # check that user is redirected from review game page if not logged in
    response = client.post('/game_info/review_game')
    assert response.headers['Location'] == '/authentication/login'


def test_review(client, auth):
    # Login a user.
    auth.login()

    # Check that we can retrieve the review page.
    response = client.get('/game_info/review_game?game_id=763550').status_code
    assert response == 200

    # check that user is redirected to game info page with correct game after posting review
    response = client.post(
        '/game_info/review_game?game_id=763550',
        data={'comment': 'test review', 'rating': '5'}
    )
    assert response.headers['Location'] == '/game_info?game_id=763550'


def test_game_library(client):
    # check that we can retrieve the game library page
    response = client.get('/game_library?current_page=0')
    assert response.status_code == 200


def test_login_required_to_favourite(client):
    # check user is redirected to login page if game favourited while not logged in
    response = client.get('/game_info/favourite_game')
    assert response.headers['Location'] == '/authentication/login'


def test_favourite(client, auth):
    auth.login()

    # check client is redirected to corresponding game info page once game is favourited
    response = client.get('/game_info/favourite_game?game_id=763550')
    assert response.headers['Location'] == '/game_info?game_id=763550'
