#!/usr/bin/env python3

#=================================================================d======
#                        General Documentation

"""CSS458 Midterm Problem 3 - Martin L. Metke
Rejection Method
2017/04/27
"""
#---------------- Module General Import and Declarations ---------------
import numpy as np
import numpy.ma as ma
import matplotlib.pyplot as plt
import sys

#------------------------- User Editable -------------------------------
# Have to reset recursion limit to prevent stack trace
sys.setrecursionlimit(2000)

XMIN = 0
XMAX = 1.0
XRES = 100
RANDCOUNT = 5000
FBOUND = 2.0

#---------------------- General Functions: func -----------------------
def func(x):
    """Function for rejection method
    """
    return np.where(x<0.5, 1.75, 0.25)


#---------------------- General Functions: rej -----------------------
def rej(npts, randVals = None, yfunc = func):
    """Element-wise rejection method.
    
    Args:
        npts (int):             Length of array to generate
        randVals (maskedarray): Masked ndarray (for recursion)
        yfunc (function):       Function to use as rejection check
    """
    # Bound numbers to compare against
    randBound = np.random.uniform(0, FBOUND, npts)

    # If this is the first pass, instantiate randVals as RANDCOUNT random
    # values in the range of [XMIN, XMAX) and convert to a masked array
    if randVals is None:
        # First pass at random values
        randVals = ma.asarray(np.random.uniform(XMIN, XMAX, npts))
        # Harden the mask so that masked values cannot be reassigned
        randVals.harden_mask()

    else:
        # Apply the yfunc to all unmasked (bad) values to retry generating
        # values of f(x) > [0, FBOUND)
        # ma.apply_along_axis(lambda x: random.uniform(XMIN, XMAX), 0, randVals)
        badSize = len(randVals[func(randVals) <= randBound])
        randVals[func(randVals) <= randBound] = \
                np.random.uniform(XMIN, XMAX, badSize )
    
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
    results = rej(1000)

    # Plot a histogram of the x values which were returned
    ax2 = ax1.twinx()
    ax2.hist(results, bins=XRES, normed=False, facecolor='red', alpha=0.75)
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
