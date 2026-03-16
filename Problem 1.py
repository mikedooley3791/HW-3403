#region problem statement
r'''
chatGpt was used to develop and troubleshoot this program
	(50 pts) Create a Python program that simulates an industrial-scale gravel production process where crushed rocks
	are sieved through a pair of screens:  the first screen is a large aperture screen that excludes rocks above a
	certain size and the second screen has a smaller aperture.  The product is the fraction of rocks from between the screens.

Assumptions:
	While the actual gavel is not spherical, we will assume that the rocks are spherical.
	Prior to sieving, the gravel follows a log-normal distribution (i.e., loge(D) is N(μ,σ)), where D is the rock
	diameter, μ=mean of ln(D) and σ= standard deviation of ln(D).  After sieving, the log-normal distribution is now
	truncated to have a maximum (Dmax) and minimum size (Dmin) imposed by the aperture size of the screens.

Your program should solicit input from the user (with suggested default values) μ, σ, Dmax and Dmin.  It should then
produce 11 samples of N=100 rocks randomly selected from the truncated log-normal distribution and report to the user
through the cli the sample mean (D̅) and variance (S2) of each sample as well as the mean and variance of the sampling mean.

Note:
The standard log-normal probability density function (PDF) is normalized over (0,∞) by:
f\left(D\right)=\frac{1}{D\sigma\sqrt{2\pi}}e^{-\frac{\left(ln\left(D\right)-\mu\right)^2}{2\sigma^2}};\int_{0}^{\infty}f\left(D\right)dD=1

And the normalized truncated log-normal PDF is given by:
f_{trunc}\left(D\right)=\frac{f\left(D\right)}{F\left(D_{max}\right)-F\left(D_{min}\right)}

Your grade will be based on your efficient use of imports of the allowed modules, use of functions and function calls,
use of lists and list comprehensions, your clarity in your docstrings and comments and your overall approach to the
problem.  Clearly state your assumptions in the docstring of the main function.
'''
#endregion

#region imports
import math
import numpy as np
from random import random as rnd
from scipy.integrate import quad
from scipy.optimize import fsolve
#endregion

#region functions
def ln_PDF(args):
    '''
    chatGpt was used to develop and troubleshoot this program
    Compute teh standard log-normal probability density function
    :param args: tuple (D, mu, sig)
    :return: Float value of the log-normal PDF at D
    '''
    D, mu, sig = args
    if D <= 0.0:
        return 0.0
    p = 1/(D*sig*math.sqrt(2*math.pi))
    exponent = -((math.log(D)-mu)**2)/(2*sig**2)
    return p*math.exp(exponent)

def ln_CDF(args):
    """
    chatGpt was used to develop and troubleshoot this program
    Finds teh cumulative distribution function of the log normal distribution using numerical integration.
    :param args: tuple (D,mu,sig)
    :return float probability that a rock diameter is less than D
    """
    D, mu, sig = args
    val, _ = quad(lambda x: ln_PDF((x,mu,sig)), 0, D)
    return val
def tln_PDF(args):
    """
    chatGpt was used to develop and troubleshoot this program
    Finds the truncated log normal probability density function
    :param args: tuple (D, mu, sig, F_DMin, F_DMax)
    :return: float value of truncated PDF
    """
    D,mu,sig,F_DMin,F_DMax = args
    return ln_PDF((D,mu,sig))/(F_DMax-F_DMin)

def F_tlnpdf(args):
    '''
    chatGpt was used to develop and troubleshoot this program
    Calculates Truncated Cumulative probability
    :param args: tuple (mu, sig, D_Min, D_Max, D, F_DMax, F_DMin)
    :return float probability from D_Min to D
    '''
    mu, sig, D_Min, D_Max, D, F_DMax, F_DMin = args
    if D <= D_Min:
        return 0
    if D >= D_Max:
        return 1
    val,_ = quad(lambda x: tln_PDF((x,mu,sig,F_DMin,F_DMax)),D_Min,D)
    return val

def makeSample(args, N=100):
    """
    chatGpt was used to develop and troubleshoot this program
    Generates a sample of rock diameters using inverse transform sampling
    :param args: tuple (ln_Mean, ln_sig, D_Min, D_Max, F_DMax,F_DMin)
    N = int sample size
    :return list of rock diameters
    """
    ln_Mean, ln_sig, D_Min, D_Max, F_DMax, F_DMin = args # unpack args
    # use random to produce uniformly distributed probability values and the truncated log-normal PDF to get values for D
    probs = [rnd() for _ in range(N)]  # the uniformly random list of probabilities
    # using Secant and a lambda function that equates to zero when the proper value of D is chosen:  integral(f_trunc, D_Min, D) - P
    # I'm doing this inside a list comprehension, but it could be done with a regular function and a for loop.
    d_s = []
    for p in probs:
        func = lambda D: F_tlnpdf((ln_Mean,ln_sig,D_Min,D_Max,D[0], F_DMax,F_DMin))- p
        guess = np.array([(D_Min+D_Max)/2])
        root = fsolve(func,guess)[0]
        d_s.append(root)
    return d_s

def sampleStats(D, doPrint=False):
    """
    chatGpt was used to develop and troubleshoot this program
    Finds sample mean and variance
    D: list data values
    doPrint: bool Print stats if true
    :return tuple(mean,variance)
    """
    arr = np.array(D)
    mean = np.mean(arr)
    var = np.var(arr, ddof=1)
    if doPrint:
       print(f"mean = {mean:.3f}, var = {var:.3f}")
    return mean, var

def getFDMaxFDMin(args):
    """
    chatGpt was used to develop and troubleshoot this program
    Finds F(Dmin) and F(Dmax) for the original log normal distribution
    param args: tuple (mean_ln,sign_ln,D_Min,D_Max)
    :return tuple(F(Dmin),F(Dmax))
    """
    mean_ln, sig_ln, D_Min, D_Max = args
    F_DMin = ln_CDF((D_Min, mean_ln,sig_ln))
    F_DMax = ln_CDF((D_Max, mean_ln,sig_ln))

    return F_DMin, F_DMax

def makeSamples(args):
    """
    chatGpt was used to develop and troubleshoot this program
    Generates all samples and calculates sample means.
    :param args: tuple (mean_ln,sig_ln,D_Min,D_Max,F_DMax,F_DMin,N_sampleSize,N_samples,doPrint)
    :return turple (Samples, Means)
    """
    mean_ln, sig_ln, D_Min, D_Max, F_DMax, F_DMin, N_sampleSize, N_samples, doPrint = args
    Samples = []
    Means = []
    for n in range(N_samples):
        # Here, I am storing the computed probabilities and corresponding D's in a tuple for each sample
        sample = makeSample((mean_ln, sig_ln, D_Min, D_Max, F_DMax, F_DMin), N=N_sampleSize)
        Samples.append(sample)
        # Step 3:  compute the mean and variance of each sample and report to user
        mean,var = sampleStats(sample)
        Means.append(mean)

        if doPrint == True:
            print(f"Sample {n+1}: mean = {mean:0.3f}, var = {var:0.3f}")
    return Samples, Means

def main():
    '''
    chatGpt was used to develop and troubleshoot this program
    Simulates an industrial gravel production process.
    Rock diameter initally follow a log normal distribution
    Two sieves truncate the distribution between Dmin and Dmax
    The program generates 11 samples of 100 rocks from the truncated distribution and reports mean and variance of each sample and the mean and variance of the sample mean.
    Assumptions:Rocks are spheres
                ln(D) follows normal distribution
    '''
    # setup some default values
    mean_ln = math.log(2)  # units are inches
    sig_ln = 1
    D_Max = 1
    D_Min = 3.0/8.0
    N_samples = 11
    N_sampleSize = 100
    F_DMin,F_DMax = getFDMaxFDMin((mean_ln,sig_ln,D_Min,D_Max))
    Samples, Means = makeSamples((mean_ln, sig_ln, D_Min, D_Max, F_DMax, F_DMin, N_sampleSize, N_samples, True))
    stats_of_Means = sampleStats(Means)
    print("\nResults for Sampling Means")
    print(f"Mean of the sampling mean:  {stats_of_Means[0]:0.3f}")
    print(f"Variance of the sampling mean:  {stats_of_Means[1]:0.6f}")

#endregion

if __name__ == '__main__':
    main()