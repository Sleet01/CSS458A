#=============================================================================
# CSS458 Week 5 Homework - Estimating Customer Flow
#
# Python implementation of Maki/Thompson customer flow model.
# https://canvas.uw.edu/courses/1151937/files/41412929/download?wrap=1
#
# By Martin Metke
# April 25, 2017
#
# Notes:
# - Adapted for Python 3.6
# - About animation in matplotlib:
#   http://wiki.scipy.org/Cookbook/Matplotlib/Animations
#   http://matplotlib.org/api/pyplot_api.html#matplotlib.pyplot.plot
#   http://stackoverflow.com/questions/12822762/pylab-ion-in-python-2-
#       matplotlib-1-1-1-and-updating-of-the-plot-while-the-pro
#=============================================================================

#========================= IMPORTED MODULES (begin) ==========================

import time
import numpy as N
import matplotlib.pyplot as plt
import math

#========================= IMPORTED MODULES  (end)  ==========================

#========================== USER ADJUSTABLE (begin) ==========================
N_TESTS = 100 #- number random walk tests
N_STEPS = 50  #- max. number of random walk steps to see how mean distance
              #  behaves
NMUS = N.array([10, 10, 15, 15, 5, 5, 5, 5, 5, 5, 5, 5, 15, 15, 15, 15, 15, 15,
    10, 10], dtype='d')
NSIGMAS = N.array([2.3, 2.3, 2.8, 2.8, 1.6, 1.6, 1.6, 1.6, 1.6, 1.6, 1.6, 1.6,
    2.8, 2.8, 2.8, 2.8, 2.8, 2.8, 2.3, 2.3], dtype="d")
NCASUALS = N.array([100, 100, 150, 150, 50, 50, 50, 50, 50, 50, 50, 50, 150,
    150, 150, 150, 150, 150, 100, 100], dtype="d") 
#=========================== USER ADJUSTABLE (end) ===========================

def npFromMuSigma(mu, sigma):

    n = N.power(mu, 2) / (mu - N.power(sigma, 2))
    p = mu / n
    print("Types of n, p: ", n.dtype, p.dtype)

    return (n, p)

def main():

    for i in range(len(NCASUALS)):
        pass

    coreN, coreP = npFromMuSigma(NMUS, NSIGMAS)
    print("Core Customers N, P: ", coreN, coreP)
    # Broken in casting, somehow...
    # coreCustomers = N.random.binomial(coreN, coreP, (N_TESTS, len(coreN)))
    # print(coreCustomers)

if __name__ == "__main__":

    main()
