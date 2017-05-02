#!/usr/bin/env python3

# Author: Martin L. Metke
# Class: CSS 458
# Date: 2017/04/27
# Midterm Problem 2 code 
#
#
#

'''Compare System Dynamics approximation of dy/dx = -2/x**3 to analytic
function'''

# imports
import numpy as np
import matplotlib.pyplot as plt

def rate(x):
    return (-2/np.power(x,3))

def func(x):
    return np.power(np.power(x, 2), -1)

def simulate():
    '''Performs a simulation of dy/dx = -2(2/x**3) over x = [1,5] inclusive,
    starting from (x,y) = (1,1)
    
    DX = 0.01
    '''

    # One tick per 0.01 x
    Dx = 0.01

    # Span of x to simulate across
    span = 5 - 1

    numIterations = int( span / Dx) + 1
    
    # Initialization
    xList = np.zeros(numIterations, dtype='d')
    xList[0] = 1
    yList = np.zeros(numIterations, dtype='d')
    yList[0] = 1

    for i in range(1, numIterations):
        x = xList[0] + i * Dx
        xList[i] = x

        newY = yList[i-1] + (rate(x)*Dx)
        yList[i] = newY

    return [xList, yList]

# Main function (runs several passes and plots graph of balances)
def main():
    '''Run a simulation and then plot the results and the analytic function
    output against each other'''

    results = simulate()

    xvals = np.linspace(1, 5, len(results[0]))
    yvals = func(xvals)

    plt.plot(results[0], results[1], label='SD method')
    plt.plot(xvals, yvals, 'r--', label='Analytical')
    plt.xlabel( "X" )
    plt.ylabel = ( "Y" )
    plt.legend()
    plt.title( \
        "Comparison of SD to Analytical Calculation of Y = 1/(X^2)")
    plt.show()

if __name__ == "__main__":
    main()
