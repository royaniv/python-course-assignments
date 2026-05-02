#test business logic 
from funct import expgrowth

def test_funct():

    # Test case 1: Basic growth
    N0 = 100
    r = 0.05
    t = 10
    k = 0.02
    expected = N0 * (e ** ((r - k) * t))
    assert abs(expgrowth(N0, r, t, k) - expected) < 0.0001

    # Test case 2: No growth (r = k)
    N0 = 50
    r = 0.03
    t = 5
    k = 0.03
    expected = N0
    assert abs(expgrowth(N0, r, t, k) - expected) < 0.0001

    # Test case 3: Decay (k > r)
    N0 = 200
    r = 0.01
    t = 8
    k = 0.04
    expected = N0 * (e ** ((r - k) * t))
    assert abs(expgrowth(N0, r, t, k) - expected) < 0.0001
