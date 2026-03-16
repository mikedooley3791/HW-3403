# region imports
from scipy.optimize import fsolve
import matplotlib.pyplot as plt
import numpy as np
# endregion

# region functions
def circleAndParabola(vals, x1=1, y1=0, radius=4,width=0.5, offset=1):
    """
    chatGpt was used to develop and troubleshoot this program
    Define system of equations for a circle and a parabola
    Circle: (y-y1)^2 + (x-x1)^2 = radius^2
    Parabola: width*x^2 + offset
    :param vals: tuple (x,y) being tested
            x1: float x coordinate of circle center
            y1: float y coordinate of circle center
            radius: float radius of circle
            width: float coefficient on x^2 in the parabola
            offset: float vertical shift of the parabola
    :return tuple (f1val, f2val), where both are equal to zero at the intersection point
    """

    x, y = vals

    f1val = (y-y1)**2+(x-x1)**2-radius**2
    f2val = width*x**2 + offset - y
    return (f1val, f2val)
def getInputs():
    """
    chatGpt was used to develop and troubleshoot this program
    Gets user input and sets default parameters for the circle and parabola
    Default parameters:
    x1 =1
    y1 =0
    radius =4
    width =0.5
    offset =1
    :return tuple(x1,y1,radius,width,offset)
    """
    x1 = input("Enter x1 (1):").strip()
    y1 = input("Enter y1 (0):").strip()
    radius = input("Enter radius (4):").strip()
    width = input("Enter Parabola width (0.5):").strip()
    offset = input("Enter Parabola offset (1):").strip()

    x1=1 if x1 ==""else float(x1)
    y1=0 if y1 ==""else float(y1)
    radius = 4 if radius =="" else float(radius)
    width = 0.5 if width =="" else float(width)
    offset = 1 if offset =="" else float(offset)

    return x1,y1,radius,width,offset

def main():
    """
    chatGpt was used to develop and troubleshoot this program
    Use fsolve to find intersection points between a circle and a parabola
    Adjustable variables:
    1: circle center (x1, y1)
    2: circle radius
    3: parabola width
    4: parabola offset
    Prints the intersection points and plots both curces on the interval -10 to 10 for both x and y axis
    Test Case: x1 = 1, y1 = 0, radius = 4, width = 0.5, offset = 1
    """
    x1,y1,radius,width,offset = getInputs()
    #find a intersection
    xA,yA = fsolve(circleAndParabola,(-3,4),(x1,y1,radius,width,offset))
    print(f"Intersection 1: x = {xA:.6f}, y = {yA:.6f}")
    #find next intersection
    xB,yB = fsolve(circleAndParabola, (2,2),(x1,y1,radius,width,offset))
    print(f"Intersection 2: x = {xB:.6f}, y = {yB:.6f}")
    #create x values
    xvals = np.linspace(-10,10,400)
    y_parabola = np.array([width*x**2+ offset for x in xvals])
    #create circle using parameter form
    theta = np.linspace(0,2*np.pi,400)
    x_circle = x1 +radius*np.cos(theta)
    y_circle = y1 +radius*np.sin(theta)
    #plot both curves
    plt.plot(x_circle,y_circle,label='Circle')
    plt.plot(xvals,y_parabola,label='Parabola')
    #plot intersection
    plt.plot(xA, yA, marker = 'o',markerfacecolor='none',markeredgecolor='red',markersize=12)
    plt.plot(xB, yB, marker = 'o',markerfacecolor='none',markeredgecolor='blue',markersize=12)
    plt.text(xA,yA,f'({xA:.3f},{yA:.3f})')
    plt.text(xB,yB,f'({xB:.3f},{yB:.3f})')
    plt.xlabel("x")
    plt.ylabel("y")
    plt.xlim(-10,10)
    plt.ylim(-10,10)
    plt.axhline(0,color='black')
    plt.axvline(0,color='black')
    plt.grid()
    plt.legend()
    plt.title("Intersection of a Circle and Parabola")
    plt.show()
# endregion

# region function calls
if __name__ == "__main__":
    main()
# endregion