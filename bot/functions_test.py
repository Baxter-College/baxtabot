'''
Test file for functions in functions.py (that are testable...)
'''

from bot.functions import findMeal, findTime, extractName
import bot.auth

def test_findMeal():
    assert findMeal('What is for dinner') == 'dinner'
    assert findMeal('I hope breakfast is good today') == 'breakfast'
    assert findMeal('tell me what is lunch') == 'lunch'

def test_findTime():
    pass

def test_extractName():
    pass

def test_extractRessieFromCSV():
    pass

def test_auth():
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
