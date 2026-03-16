#region imports
import math
from NumericalMethods import Secant
#endregion

#region function definitions
def fn1(x):
    return x-3*math.cos(x)

def fn2(x):
    return x - 3 * math.cos(2*x)*x**3

def main():
    """
       fn1:  x-3cos(x)=0; with x0=1, x1= 2, maxiter = 5 and xtol = 1e-4
       fn2:  cos(2x)*x**3; with x0=1, x1= 2, maxiter = 15 and xtol = 1e-8
       fn2:   with x0=1, x1= 2, maxiter = 3 and xtol = 1e-8

       I observe that for functions 2 and 3, the answer should be pi/2 or about 1.57
    :return: nothing, just print results
    """
    r1 = Secant(fn1, 1, 2, 5,1e-4)
    r2 = Secant(fn2, 1,2,15, 1e-8)
    r3 = Secant(fn2,1,2,3,1e-8)
    print("root of fn1 = {root:0.4f}, after {iter:0d} iterations".format(root=r1[0], iter=r1[1]))
    print(f"fn1({r1[0]:0.3f})={fn1(r1[0]):0.3f}")
    print("root of fn2 = {root:0.4f}, after {iter:0d} iterations".format(root=r2[0], iter=r2[1]))
    print(f"fn2({r2[0]:0.3f})={fn2(r2[0]):0.3f}")
    print("root of fn2 = {root:0.4f}, after {iter:0d} iterations".format(root=r3[0], iter=r3[1]))
    print(f"fn2({r3[0]:0.3f})={fn2(r3[0]):0.3f}")
#endregion

if __name__=="__main__":
    main()