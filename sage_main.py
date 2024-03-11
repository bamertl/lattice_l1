from sage.all import *
from src import my_module
from lll import my_lll
import numpy as np



def one_test(m):
    MY_MLLL = my_lll.lll_reduction(m)
    SAGE_MLLL = np.array(m.LLL())
    print(MY_MLLL)
    print(SAGE_MLLL)
    # assert that the matrixes are equal, simply assert doesn't work here
    assert (MY_MLLL == SAGE_MLLL).all()


def test_custom_lll():
    print("hi")
    for i in range(10):
        print(i)
        m = random_matrix(ZZ, 3, 3)
        one_test(m)    


test_custom_lll()