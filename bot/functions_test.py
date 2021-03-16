'''
Test file for functions in functions.py (that are testable...)
'''

from bot.functions import findMeal, findTime, extractName
import bot.auth as auth
import bot.models as models
from bot.testutils import clear

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
