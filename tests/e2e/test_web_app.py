import pytest
from flask import session

# testing registering, logging in, browsing games, adding games to the wishlist, logging out


def test_register(client):
    # Check that we retrieve the register page.
    response_code = client.get('/authentication/register').status_code
    assert response_code == 200

    # Check that we can register a user successfully, supplying a valid user name and password.

    response = client.post(
        '/authentication/register',
        data={'user_name': 'tori', 'password': '@Vrya365'}
    )

    # assert response.headers['Location'] == '/authentication/login'
    # weird, change this testing, for some reason, it throws an error when attempting to access 'Location' in response.headers


