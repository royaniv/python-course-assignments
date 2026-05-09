#test business logic 
from funct import expgrowth

def test_no_growth():
    assert expgrowth(50, 0.03, 5, 0.03) == 50

def test_decay():
    assert expgrowth(200, 0.01, 8, 0.04) < 200

