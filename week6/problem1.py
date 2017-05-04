#!/usr/bin/env python3

# problem1.py
# 
# Author: Martin Metke
# Date: 2017/05/03
# For: CSS458A Week 6 Problem1
#
# Re-write of diffusion system with stochastic heat diffusion.
#
# Adapted from:
# Headers provided on CSS458A Sp 2017 GitHub repository
# __author__ = 'v-caearl'

#============================= IMPORTS =======================================
import numpy as np
from matplotlib import pyplot as plt
#============================= END IMPORTS ===================================


#========================== USER ADJUSTABLE (begin) ==========================
# Global temperature values, in degrees C
# Constraint: COLD <= AMBIENT <= HOT
COLD = 0.0
AMBIENT = 25.0
HOT = 50.0
#=========================== USER ADJUSTABLE (end) ===========================


def diffusion(diffusionRate, site, N, NE, E, SE, S, SW, W, NW):
    """Apply diffusion of heat rate from Moore neighborhood to the
    site passed in, using a stochastic method: random normally-
    distributed numbers centered at 0.0 with STDDEV 0.5.
    Since the final neighbor coefficients must sum to 1.0, we adjust
    the random number range so that it sums to 0.0"""

    # Convert neighbor values to an ndarray for element-wise operations
    neighVals = np.array([N, NE, E, SE, S, SW, W, NW], dtype='f')
        
    # Generate random normal distribution, then create coeffecients of form
    # "(1 + rndi)*r".
    rndi = np.random.normal(0.0, 0.5, (8,))
    coeffs = ((rndi + 1) * diffusionRate)
    
    # The sum of all coefficients must equal 1, so subtract the sum of 
    # the neighbors' coefficients from 1, multiply site by the result, 
    # then add stochasticly modified neighboring sites' values.
    return(1-np.sum(coeffs))*site + np.sum(coeffs*neighVals)

def initBar(m, n, hotSites, coldSites):
    """ Set up the m x n grid of temperatures.  Cells with coords in 'hotSites'
    have the global value HOT; cells with coordinates in coldSites have the
    global value COLD; all other cells have the value AMBIENT.

    Args:
        m, n (positive int):    length and height of grid
        hotSites (list):        List of coordinates of "HOT" cells
        coldSites (list):       List of coordinates of "COLD" cells
                
    Returns:
        bar (matrix):           m x n matrix of temperatures

    """

    # Initialize grid of m x n
    ambientBar = np.zeros((m, n), dtype='l')
    ambientBar.fill(AMBIENT)
    return applyHotCold(ambientBar, hotSites, coldSites)

def applyHotCold(bar, hotSites, coldSites):
    " Function to accept a grid of temperatures and to return a grid with heat
    and cold applied at hotSites and coldSites, respectively"""

    newBar = np.copy(bar)

    for coord in hotSites:
        newBar[coord[0], coord[1]] = HOT

    for coord in coldSites:
        newBar[coord[0], coord[1]] = COLD

    return newBar

if __name__ == "__main__":

    print("Test diffusion value: ", \
            diffusion(0.1, 10, 5, 7, 7, 8, 9, 10, 8, 6))
