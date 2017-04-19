#!/usr/bin/env python3

#=================================================================d======
#                        General Documentation

"""CSS458 Randomness 1 Problem 3 - Martin L. Metke
S&S 9.2.3 Exercise 6 - Rejection Method
"""
#---------------- Module General Import and Declarations ---------------
import numpy as np
import numpy.ma as ma
import math
import random
import matplotlib.pyplot as plt
import sys

#------------------------- User Editable -------------------------------
# Have to reset recursion limit to prevent stack trace
sys.setrecursionlimit(2000)

XMIN = 0
XMAX = 0.25
XRES = 100
RANDCOUNT = 1000
FBOUND = 2 * math.pi

#---------------------- General Functions: func -----------------------
def func(x):
    """Function for fig 9.3.12
    """
    return 2 * math.pi * np.sin( 4 * math.pi * x)

#---------------------- General Functions: rej -----------------------
def rej(randVals = None, yfunc = func):
    """S&S exercise 6, rejection method.
    I have chosen to implement this as an element-wise method, for funsies.
    
    Args:
        randVals (maskedarray): Masked ndarray (for recursion)
        yfunc (function):       Function to use as rejection check
    """
    # If this is the first pass, instantiate randVals as RANDCOUNT random
    # values in the range of [XMIN, XMAX) and convert to a masked array
    if randVals is None:
        # First pass at random values
        randVals = ma.asarray(np.random.uniform(XMIN, XMAX, RANDCOUNT))
        # Harden the mask so that masked values cannot be reassigned
        randVals.harden_mask()

    else:
        # Apply the yfunc to all unmasked (bad) values to retry generating
        # values of f(x) > [0, FBOUND)
        ma.apply_along_axis(lambda x: random.uniform(XMIN, XMAX), 0, randVals)

        
    # Bound numbers to compare against
    randBound = np.random.uniform(0, FBOUND, RANDCOUNT)
    
    # Apply masking to protect valid values
    randVals = ma.masked_where(func(randVals) > randBound, randVals)

    # If all numbers are masked, that is, all values have been found to 
    # have f(randVals) greater than randBound, unmask and return the ndarray
    if randVals.count() == 0:
        randVals.soften_mask()
        randVals.mask = ma.nomask
        return randVals
    # Otherwise, attempt to fix any unmasked values by calling rej with the
    # masked array as an argument.  Ideally, only unmasked values will be
    # recalculated.
    else:
        return rej(randVals=randVals)


#---------------------- General Functions: main -----------------------
def main():
    """Plot rejection method function and perform rejection method on random
    values in the range requested.
    """

    fig, ax1 = plt.subplots()

    # Plot rejection function
    xvals = np.linspace(XMIN, XMAX, num=XRES, endpoint=True)
    yvals = func(xvals)
    ax1.plot(xvals, yvals)
    ax1.set_xlabel("X (%2f to %2f)" % (XMIN, XMAX))
    ax1.set_ylabel("Y")
    ax1.tick_params('y', colors='b')

    # Run recursive rejection
    results = rej()

    # Plot a histogram of the x values which were returned
    ax2 = ax1.twinx()
    ax2.hist(results, bins=XRES, normed=True, facecolor='red', alpha=0.75)
    ax2.set_ylabel("Count")
    ax2.tick_params('y', colors='r')

    fig.tight_layout()
    # fig.suptitle("Histogram of X values vs Rejection function")
    plt.title("Histogram of X values vs Rejection function")
    plt.show()

if __name__ == "__main__":
    print( "WARNING: May crash if rejection continues too long.  Please rerun if this occurs.")
    # The recursion limit has been tuned deeper, but it's still possible
    # (thanks, RNG!) to exceed it.  In that case, retry.
    while True:
        try:
            main()
            sys.exit(0)
        except RecursionError as e:
            print("Hit recursion limit; retrying!")
