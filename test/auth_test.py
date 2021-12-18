import bot.auth as auth
from bot.testutils import clear
from bot.error import InputError


def test_auth():
    clear()
    # Testing register and authentication works
    result = auth.auth_register('nick.p@gmail.com', 'abc123', 'Nick Patrikeos')
    assert result
    assert auth.authenticate_token(result['token']) == result['u_id']

    # Test logout works
    assert auth.auth_logout(result['token']) == {'is_success': True}
    assert not auth.authenticate_token(result['token'])

    # Test logging back in works
    login_result = auth.auth_login('nick.p@gmail.com', 'abc123')
    assert login_result
    assert auth.authenticate_token(login_result['token']) == result['u_id']


def test_auth_multiple_users():
    pass


def test_auth_register_invalid_email():
    pass


def test_auth_register_empty_password():
    pass


def test_auth_register_short_name():
    pass


def test_auth_register_long_name():
    pass


def test_auth_register_already_registered():
    pass


def test_auth_register_links_to_ressie():
    pass


def test_auth_login_success():
    pass


def test_auth_login_multiple_users():
    pass


def test_auth_login_invalid_email():
    pass


def test_auth_login_invalid_password():
    pass


def test_auth_login_both_invalid():
    pass


def test_auth_logout_success():
    pass


def test_auth_logout_invalid_token():
    pass
