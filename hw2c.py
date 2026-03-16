# region imports
from copy import deepcopy
from NumericalMethods import GaussSeidel, Transpose
from Gauss_Elim import AugmentMatrix, MatrixMultiply
# endregion
'''
This program solves two systems of linear equations using Gauss-Seidel Method 
Step:
1: Define coefficients for first matrix A then its b vector. 
(important to get the largest numbers going to down the diagonal)
2: Create the Augmented Matrix [A|B].
3: Use the Gauss-Seidel method to solve for the solution vector x.
4: Multiply A*x to verify that the results match with the original b vector. 
'''
def main():
    A=[[3,1,-1], #Matrix A (arranged so diagonal is largest number)
       [1,4,1],
       [2,1,2]]
    b = [2,12,10] #Vector b
    Aaug = AugmentMatrix(A,b) #makes augmented matrix
    x = GaussSeidel(Aaug,[0,0,0],30) #solves GaussSeidel method using initial guesses of [0,0,0] and runs the interation 30 times
    x_col =[[val] for val in x] #converts x vector into column vector
    b_check = MatrixMultiply(A,x_col) #reprduces b vector if correct
    print([round(val,3) for val in x])
    print(b_check)
    AA = [[9,2,3,4], #Second Matrix (arranged so diagonal is largest number)
          [1,-10,2,4],
          [-1, 2, 7, 3],
          [3,1,4,12]]

    bb = [2,12,21,37] #Second Vector B
    AAug = AugmentMatrix(AA,bb)#makes second augmented matrix
    xx = GaussSeidel(AAug,[0,0,0,0], 30) #solves GaussSeidel method 2nd time using initial guesses of [0,0,0] and runs the interation 30 times
    xx_col = [[val] for val in xx] #converts xx vector into column vector
    bb_check = MatrixMultiply(AA,xx_col) #reprduces bb vector if correct
    print([round(val, 3) for val in xx])
    print(bb_check)
if __name__=="__main__":
    main()