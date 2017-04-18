#!/usr/bin/env python3

#=======================================================================
#                        General Documentation

"""CSS458 Randomness 1 Problem 3 - Martin L. Metke
S&S 9.2.3 Exercise 6 - Rejection Method
"""
#---------------- Module General Import and Declarations ---------------
import numpy as np
import numpy.ma as ma
import math
import matplotlib.pyplot as plt

#------------------------- User Editable -------------------------------
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
    """
    if randVals == None:
        # First pass at random values
        randVals = ma.asarray(np.random.uniform(XMIN, XMAX, RANDCOUNT))
        randVals = yfunc(randVals)
        randVals.harden_mask()
    else:
        ma.apply_along_axis(yfunc, 0, randVals)
    # Bound numbers to compare against
    randBound = np.random.uniform(0, FBOUND, RANDCOUNT)
    
    # Apply masking to protect valid values
    randVals = ma.masked_where(randVals > randBound, randVals)
    print("Count remaining: ", randVals.count())
    if randVals.count() == 0:
        randVals.soften_mask()
        randVals.mask = ma.nomask
        return randVals
    else:
        return rej(randVals=randVals)


#---------------------- General Functions: main -----------------------
def main():
    """Plot rejection method function and perform rejection method on random
    values in the range requested.
    """
    xvals = np.linspace(XMIN, XMAX, num=XRES, endpoint=True)
    yvals = func(xvals)
    plt.plot(xvals, yvals)
    plt.draw()
    rej()
    plt.show()

if __name__ == "__main__":
    
    main()
