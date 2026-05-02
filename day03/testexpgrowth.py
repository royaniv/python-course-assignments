#examples for assert statements in expgrowth calculation input, sysargv, GUI
#for input

import expgrowcalc_input
import expgrowcalc_sysargv


def test1():
    assert expgrowcalc_input(2, 0.05, 10, 0.02) == 2.6997176151520064

#for sysargv
def test2():
    assert expgrowcalc_sysargv(2, 0.05, 10, 0.02) == 2.6997176151520064