#!/usr/bin/env python3

#=======================================================================
#                        General Documentation

"""CSS458 Randomness 1 Problem 2 - Martin L. Metke

Create pairs of coordinates within a desired normal distribution,
based on teh Box-Muller-Gauss Method.  From S&S 9.2.3 Ex 2.
"""
#------------------------- User Editable -------------------------------
MAIN_MEAN = 9
MAIN_SIGMA = 2
MAIN_COUNT = 30

#---------------- Module General Import and Declarations ---------------
import numpy as np
import math
import matplotlib.pyplot as plt


#---------------------- General Functions: BMGM -----------------------
def BMGM( mean, sigma, size ):
    """Box-Muller-Gauss Method to generate a normal distribution within
    a given range.
    
    Args:
        mean (int or float):    Mean of the desired distribution
        sigma (int or float):   Standard deviation of desired distribution
        size (int):             Number of random numbers user needs
    Returns: 
        coords (list):          list of arrays of numbers in distribution
    
    """
    a = np.random.uniform(low=0.0, high=math.pi*2, size=(size,))
    b = sigma * np.sqrt(-2 * np.log(np.random.uniform(0, 1, size)))
    return np.column_stack((b*np.sin(a) + mean, b*np.cos(a) + mean))


#---------------------- General Functions: main -----------------------
def main():
    """Creates a distribution based on the requirements of S&S 9.2.3 ex 2.
    BMGM can be called with arbitrary values, or the main function's defaults
    can be editied above.
    """
    
    results = BMGM(MAIN_MEAN, MAIN_SIGMA, MAIN_COUNT)
    print("BMG method normal distribution of mean %s, sigma %s" % \
        (MAIN_MEAN, MAIN_SIGMA))
    print(results)

#    plt.plot(results[0], results[1])
#    plt.xlabel("Sin")
#    plt.ylabel("Cos")
#    plt.title( "Box-Muller-Gauss distribution" )
#
#    plt.show()

    return 0

if __name__ == "__main__":
    
    main()
