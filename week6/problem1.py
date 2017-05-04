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

import numpy as np
from matplotlib import pyplot as plt

def diffusion(diffusionRate, site, N, NE, E, SE, S, SW, W, NW):
    """Apply diffusion of heat rate from Moore neighborhood to the
    site passed in, using a stochastic method: random normally-
    distributed numbers centered at 0.0 with STDDEV 0.5.
    Since the final neighbor coefficients must sum to 1.0, we adjust
    the random number range so that it sums to 0.0"""

    # Convert neighbor values to an ndarray for element-wise operations
    neighVals = np.array([N, NE, E, SE, S, SW, W, NW], dtype='f')
        
    # Generate random normal distribution
    rndi = np.random.normal(0.0, 0.5, (8,))
    
    # Adjust entire set of random numbers so that it sums to 0.0, +-
    # 1E-16 or so.
    rndi -= np.sum(rndi)/8.0

    # Finalize coefficient generation
    coeffs = (rndi + 1)*diffusionRate

    return(1-8*diffusionRate)*site + np.sum(coeffs*neighVals)
