from sage.all import *
from src import my_module
from lll import my_lll


def main():
    M = Matrix(ZZ, [[1, 2, 3], [2, -1, 1], [3, 0, 1]])

    # Apply the LLL algorithm to the basis
    M_LLL = M.LLL()

    MY_MLLL = my_lll.lll_reduction(M)
    # Print the original and LLL-reduced basis
    print("Original basis:")
    print(M)
    print("\nLLL-reduced basis:")
    print(M_LLL)    
    print(MY_MLLL)
main()