#!/usr/bin/env python3

#=======================================================================
#                        General Documentation

"""CSS458 Randomness 1 Problem 1 - Martin L. Metke
"""
#---------------- Module General Import and Declarations ---------------
import numpy as np
import math
import matplotlib.pyplot as plt


#---------------------- General Functions: func -----------------------
def func( x ):
    """function used to plot curve in S&S 9.2.1
    
    Args:
        x (int or float): number to operate on

    Returns: 
        y: sqrt(cos^2(x) + 1)
    
    """
    return math.sqrt(math.cos(x)*math.cos(x) + 1)

def simulate(darts_count, passes=100, ranges=[0.0, 2.0, 0.0, 1.5], yfunc=func):
    '''Run one set of Monte Carlo simulations for "dartboard" that contains
    a section of the provided yfunction (e.g. y = yfunc(x) continuously within
    the ranges of x and y provided in ranges).  Based on in-class solution.

    Args:
        darts_count (int):  Number of darts to "throw" each pass
        passes (int):       Number of simulation runs to execute
        ranges (list):      [xmin, xmax, ymin, ymax] extents to "throw" at
        yfunc (function):   Function of (x) to use to find y

    Returns:
        MeanAndStdDev (dict): dictionary of results 'Mean' and 'StdDev'
    
    '''

    # Calculate the size of the rectangle
    rectangle = (ranges[1]-ranges[0]) * (ranges[3] - ranges[2])

    # Set of area calculations to record Monte Carlo approximations
    areas = np.zeros(passes, dtype='f')

    # Do <passes> number of passes
    for i in range(passes):
        
        # Create two sets of random values to use as coordinates for Monte Carlo
        x_vals = \
            np.random.random(darts_count) * (ranges[1] - ranges[0]) + ranges[0]
        y_vals = \
            np.random.random(darts_count) * (ranges[3] - ranges[2]) + ranges[2]

        # A set of y values calculated from the function.
        funcy_vals = np.zeros(darts_count, dtype='f')

        for j in range(darts_count):

            funcy_vals[j] = yfunc(x_vals[j])
        
        # Set this pass's area 
        areas[i] = rectangle * \
            np.sum( np.where( y_vals < funcy_vals, 1, 0), dtype='f') / \
                    float(darts_count)

        
    # Package mean and stddev in a dict
    return {'Mean': np.mean(areas), \
            'StdDev': np.std(areas)}


def main():
    darts_set = np.array([10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000])
    est_areas = []
    est_std = []

    # Test various numbers of darts
    for darts in darts_set:

        print( "Darts: %s" % (darts))

        # Call simulate with each successive value and print output
        retval = simulate(darts) # Default vals are otherwise fine
        print( "Mean, std dev of area: %f, %f" % (retval['Mean'], \
                retval['StdDev']))

        # Add mean area to est_areas
        est_areas.append(retval['Mean'])
        est_std.append(retval['StdDev'])

    # plt.plot(darts_set, np.array(est_std))

    return 0

if __name__ == "__main__":
    
    main()
