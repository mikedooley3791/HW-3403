#region imports
from math import sqrt, pi,gamma
from turtle import TurtleGraphicsError

from NumericalMethods import Simpson
#endregion

#region function
def TPDF(args):
    '''
    chatGpt was used to develop and troubleshoot this program
    T probability density function
    :param args: tuple (u,m)
                u = value where teh pdf is evaluated
                m = degrees  of freedom
    :return: value of t pdf at u
    '''
    u, m = args

    Km = gamma(.5*m+.5)/(sqrt(m*pi)*gamma(.5*m))
    return Km*(1+(u**2)/m)**(-(m+1)/2)

def TCDF(z,m):
         """
         chatGpt was used to develop and troubleshoot this program
         Computes F(z) = P(T<=z) for t probability variable with m degree of freedom using simpsons rule.        
         :param z: upper limit of integration
         :param m: degree of freedom
         :return: probability F(z)
         """
         lhl = -100
         rhl = z
         return Simpson(TPDF,(m,lhl,rhl),N=1000)
def main():
    '''
    chatGpt was used to develop and troubleshoot this program
    This program asks the user for degrees of freedom and a z value then computes the t distribution probability F(z)
    '''
    again = True
    yesOptions = {"yes","y","true","ok"}

    m = 7
    z = 0.0

    while again:
        response = input(f"Enter Degree of Freedom of ({m}):").strip()
        m = int(response) if response != "" else m
        response =input(f"Enter z value ({z:0.3f}):").strip()
        z = float(response) if response != "" else z
        prob = TCDF(z,m)
        print(f"\nFor m = {m} and z = {z:0.4f}")
        print(f"F(z) = P(T<={z:0.4f}) = {prob:0.6f}")
        response =input("\nGo Again? (Y/N)").strip().lower()
        again = True if response in yesOptions else False
#endregion
#region function calls
if __name__ == "__main__":
    main()
#endregion