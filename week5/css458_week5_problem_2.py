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
N_TESTS = 1000 #- Number of tests for each N, P
NMUS = N.array([10, 10, 15, 15, 5, 5, 5, 5, 5, 5, 5, 5, 15, 15, 15, 15, 15, 15,
    10, 10], dtype='d') #- Mu value for each time step, for core customers
NSIGMAS = N.array([2.3, 2.3, 2.8, 2.8, 1.6, 1.6, 1.6, 1.6, 1.6, 1.6, 1.6, 1.6,
    2.8, 2.8, 2.8, 2.8, 2.8, 2.8, 2.3, 2.3], dtype="d") #- Core sigmas
NCASUALS = N.array([100, 100, 150, 150, 50, 50, 50, 50, 50, 50, 50, 50, 150,
    150, 150, 150, 150, 150, 100, 100], dtype="d") #- Mall customers for
                                                    # calculating casuals
#=========================== USER ADJUSTABLE (end) ===========================

def npFromMuSigma(mu, sigma):

    n = N.power(mu, 2) / (mu - N.power(sigma, 2))
    p = mu / n
    # print("Types of n, p: ", n.dtype, p.dtype)

    return (N.around(n).astype('i'), p)

def runSimulation(casP, mallFactor):

    totalCustomers = N.zeros(NCASUALS.shape, dtype='f')

    coreN, coreP = npFromMuSigma(NMUS, NSIGMAS)
    print("Core Customers N, P: ", coreN, coreP)
    
    # Create mean of 1000 tests of N core customers at P probability
    coreCustomers = N.mean(N.random.binomial(coreN, coreP, (N_TESTS,
        len(coreN))), 0)
    print("Mean number of core customers per 30 minutes", coreCustomers)
    
    # Unfortunately casual customers depend on prior customers at k-1
    casualCustomers = N.zeros((20,), dtype='f')
    casualCustomers[0] = N.mean(N.random.binomial(mallFactor * NCASUALS[0], 0.01, N_TESTS))
    print("Initial Casual Customers: ", casualCustomers[0])

    totalCustomers[0] = coreCustomers[0] + casualCustomers[0]
    print("Initial Total Customers: ", totalCustomers)
    
    # Continue filling in totalCustomers
    for i in range(1, len(NCASUALS)):
        casualCustomers[i] = N.mean(N.random.binomial(mallFactor * NCASUALS[i], \
                0.01 + casP * totalCustomers[i-1], 1000))
        totalCustomers[i] = coreCustomers[i] + casualCustomers[i]
    
    print("Final Total Customers: ", totalCustomers)

    # Return three arrays of values
    return (coreCustomers, casualCustomers, totalCustomers)

def main(casP=0.002, factor=1.0):
    '''Simulate the number of customers to visit a record shop based on some
    approximations of probabilities, binomial / Bernoulli Trials.'''

    # Run simulation once
    coreCustomers, casualCustomers, totalCustomers = runSimulation(casP,factor)
    
    # Print table 4.18
    print("\n")
    print("================================================================================")
    print("Time Seg\tMean Core\t\tMean Cas.\t\tMean Total")
    print("================================================================================")
    for j in range(len(totalCustomers)):
        print("%i\t|\t%f\t|\t%f\t|\t%f" % (j + 1, coreCustomers[j],
            casualCustomers[j], totalCustomers[j]))
    print("================================================================================")
    print("Totals:\t|\t%f\t|\t%f\t|\t%f" % (N.sum(coreCustomers),
        N.sum(casualCustomers), N.sum(totalCustomers)))
    print("================================================================================")
    
if __name__ == "__main__":

    main()
