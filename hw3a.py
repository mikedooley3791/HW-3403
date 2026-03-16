# region import
from NumericalMethods import GPDF, Probability, Simpson, Secant
# end region import

# region function
def main():
    """
    chatGpt was used to develop and troubleshoot this program
    This program uses numerical integration of the Gaussian probability density function to solve normal probability problems.
    Given cases:
    1 One-Sided given C, find P(x<c) or P(x>c)
    2 One sided given P, find C
    3 Two sided given C, find P(2*mu-c<x<c)
    4 Two sided given P find c for center interval
    """
    again = True
    yes_options = ["y","yes","true","on",]
    #starting values
    mu = 0.0
    sig = 1.0
    c = 1.0
    P = 0.5
    one_sided = True
    given_is_c = True
    greater_than = False
    while again:
        print()
        response = input (f"Enter Population Mean (mu)({mu:.3f}):").strip()
        mu = float(response) if response != "" else mu

        response = input(f"Enter Standard Deviation (sigma)({sig:.3f}):").strip()
        sig = float(response) if response != "" else sig

        response = input(f"Is it one sided?({one_sided}):").strip().lower()
        one_sided = True if response in yes_options else False if response != "" else one_sided

        response = input(f"C seeking P?({given_is_c}):").strip().lower()
        given_is_c = True if response in yes_options else False if response != "" else given_is_c
        if one_sided:
            response = input(f"Greather-Than probability?({greater_than}):").strip().lower()
            greater_than = True if response in yes_options else False if response != "" else greater_than
        else:
            response = input("Outside the center interval? (False):").strip().lower()
            greater_than = True if response in yes_options else False
# Given C wants P
        if given_is_c:
            response = input(f"Cutoff Value (C)? ({c:.3f}):").strip()
            c = float(response) if response != "" else c
            # One sided
            if one_sided:
                    prob = Probability(GPDF,(mu,sig),c,GT=greater_than)
                    if greater_than:
                        print(f"\nP(X>{c:0.4f} | mu={mu:0.4f} | sig={sig:0.4f}) = {prob:0.6f}")
                    else:
                        print(f"\nP(X<{c:0.4f} | mu={mu:0.4f} | sig={sig:0.4f}) = {prob:0.6f}")
            # Two Sided
            else:
                lower = 2*mu - c
                upper = c
                inside_prob = Simpson(GPDF,(mu,sig,lower,upper),N=1000)
                outside_prob = 1 - inside_prob

                if greater_than:
                    print(f"\nP(X < {lower:0.4f} or X > {upper:0.4f} | mu={mu:0.4f}, sigma={sig:0.4f}) = {outside_prob:0.6f}")
                else:
                    print(
                        f"\nP({lower:0.4f} < X < {upper:0.4f} | mu={mu:0.4f}, sigma={sig:0.4f}) = {inside_prob:0.6f}")
# Given P and want C
        else:
            response = input(f"Desired Probability (P)?({P:.3f}):").strip()
            P = float(response) if response != "" else P

            # One Sided
            if one_sided:
                def fn(x):
                    return Probability(GPDF,(mu,sig),x,GT=greater_than)- P
                c_sol,n_iter = Secant(fn,mu-sig,mu+sig,maxiter=50,xtol=1e-6)
                if greater_than:
                    print(f"\nCutoff c such that P(X > c | mu={mu:0.4f}, sigma={sig:0.4f}) = {P:0.6f}")
                else:
                    print(f"\nCutoff c such that P(X < c | mu={mu:0.4f}, sigma={sig:0.4f}) = {P:0.6f}")
                    print(f"c = {c_sol:0.6f}")
                    print(f"Secant Iterations = {n_iter}")
            # Two Sided
            else:
                def fn(x):
                    lower = 2*mu -x
                    upper = x
                    inside_prob = Simpson(GPDF,(mu,sig,lower,upper),N=1000)
                    outside_prob = 1-inside_prob
                    return(outside_prob-P) if greater_than else (inside_prob-P)

                c_sol,n_iter = Secant(fn,mu,mu+sig, maxiter=50, xtol=1e-6)
                lower_sol = 2*mu -c_sol

                if greater_than:
                    print(f"\nCutoff c such that P(X < {lower_sol:0.6f} or X > {c_sol:0.6f} | mu={mu:0.4f}, sigma={sig:0.4f}) = {P:0.6f}")
                else:
                    print(f"\nCutoff c such that P({lower_sol:0.6f} < X < {c_sol:0.6f} | mu={mu:0.4f}, sigma={sig:0.4f}) = {P:0.6f}")
                print(f"Upper Bound c ={c_sol:0.6f}")
                print(f"Lower Bound = {lower_sol:0.6f}")
                print(f"Secant Iterations = {n_iter}")
        print()
        response = input ("Go again?(y/n):").strip().lower()
        again = True if response in yes_options else False


# end region function

if __name__ == "__main__":
    main()