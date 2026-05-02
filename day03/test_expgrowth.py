#examples for assert statements in expgrowth calculation input, sysargv, GUI


#for input
def test_input():
    assert expgrowcalc_input(2, 0.05, 10, 0.02) == 2.6997176151520064

#for sysargv
def test_sysargv():
    assert expgrowcalc_sysargv(2, 0.05, 10, 0.02) == 2.6997176151520064

#for GUI
def test_GUI():
    assert expgrowcalc_GUI(2, 0.05, 10, 0.02) == 2.6997176151520064
    