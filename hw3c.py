#region imports
import math
import matrixOperations as mo
import DoolittleMethod
import Gauss_Seidel as GS
#endregion
#region Function
def Symmetric(A):
    """
    chatGpt was used to develop and troubleshoot this program
    Check to see if matrix is symmetric by comparing A to A^T
    :param A: square matrix
    :return:  True if A is symmetric, False otherwise
    """
    AT = mo.Transpose(A)
    return AT == A

def CholeskyFactor(A):
    """
    chatGpt was used to develop and troubleshoot this program
    Computes the Cholesky factorization A = L * L^T
    :param A: square matrix
    :return: lower triangular matrix L
    """
    n = len(A)
    L = [[0.0 for _ in range(n)] for _ in range(n)]

    for i in range(n):
        for j in range(i +1):
            sm = 0.0
            for k in range(j):
                sm += L[i][k] * L[j][k]
            if i == j:
                val = A[i][i] - sm
                if val <= 0:
                    raise ValueError("Matrix is not positive definite")
                L[i][j] = math.sqrt(val)
            else:
                L[i][j] = (A[i][j]-sm)/L[j][j]
    return L

def SymPosDef(A):
    """
    chatGpt was used to develop and troubleshoot this program
    Checks if A is symmetric positive definite
    steps:
    1: check if A is symmetric
    2:attempt Cholesky factorization if Cholesky works A is definite
    :param A: square matrix
    :return: True if symmetric postive definite, False otherwise
    """
    if not Symmetric(A):
        return False
    try:
        CholeskyFactor(A)
        return True
    except ValueError:
        return False
def Transpose(A):
    """
    chatGpt was used to develop and troubleshoot this program
    Returns the transpose of a matrix
    """
    rows = len(A)
    cols = len(A[0])
    return [[A[r][c] for r in range(rows)] for c in range(cols)]

def Cholesky(Aaug):
    """
    chatGpt was used to develop and troubleshoot this program
    Solves Ax= b using Cholesky
    steps:
    1: Separate Aaug into A and b
    2:Factor A = L*L^T
    3:Solve L*y = b
    4:Solve L^T*x = y

    :param Aaug: augmented matrix
    :return: tuple(x,L,LT)
    """
    A, b = GS.separateAugmented(Aaug)
    L = CholeskyFactor(A)
    LT = Transpose(L)

    y = DoolittleMethod.BackSolve(L,b,UT=False)
    x = DoolittleMethod.BackSolve(LT,y,UT=True)

    return (x,L,LT)

def printMatrix(M,name):
    """
    chatGpt was used to develop and troubleshoot this program
    Prints matrix with rounded entries.
    """
    print(f"{name}:")
    for row in M:
        print([round(val, 3)for val in row])
    print()

def printVector(x,name):
    """
    chatGpt was used to develop and troubleshoot this program
    Prints a column vector with rounded entries.
    """
    print(f"{name}:")
    for row in x:
        print([round(row[0],3)])
    print()

def main():
    """
    chatGpt was used to develop and troubleshoot this program
    step:
    1: define augmented matrices
    2: test whether matrix is symmetric positive definite
    3: use Cholesky if SPD otherwise Doolittle
    4: check solution by multiplying A*x
    5: print method used and solution
    """
    #Given Matrices
    Aaug1 = [[1,-1,3,2,15],
             [-1,5,-5,-2,-35],
             [3,-5,19,3,94],
             [2,-2,3,21,1]]
    Aaug2 = [[4,2,4,0,20],
             [2,2,3,2,36],
             [4,3,6,3,60],
             [0,2,3,9,122]]
    Aaug3 = [[3,-5,19,3,94], # purpose made non symmetric matrice for testing
             [-1,5,-5,-2,-35],
             [1,-1,3,2,15],
             [2,-2,3,21,1]]

    matrices = [Aaug1,Aaug2,Aaug3]

    for idx, Aaug in enumerate(matrices,start=1):
        print(f"\n Matrix {idx}:\n")
        A, b = GS.separateAugmented(Aaug)
        print("A:")
        for row in A:
            print(row)
        print("\nb:")
        print(b)
        print()

        isSPD = SymPosDef(A)

        if isSPD:
            method = "Cholesky"
            x,L,LT = Cholesky(Aaug)

            print("Matrix is symmetric positive definite.")
            print("Using Cholesky Method.\n")
            printMatrix(L,"L")
            printMatrix(LT,"LT")
        else:
            method = "Doolittle"
            x = DoolittleMethod.Doolittle(Aaug)

            print("Matrix is NOT symmetric positive definite.")
            print("Using Doolittle Method.\n")
        printVector(x,"Solution x")

        Ax = GS.matrixMult(A,x)
        printVector(Ax,"Check Ax")
        print("Method used:",method)
#endregion

if __name__ == "__main__":
    main()
