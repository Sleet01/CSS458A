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
import matplotlib.animation as animation
from matplotlib import pyplot as plt
from matplotlib.ticker import MaxNLocator
import time
#============================= END IMPORTS ===================================


#========================== USER ADJUSTABLE (begin) ==========================
# Global temperature values, in degrees C
# Constraint: COLD <= AMBIENT <= HOT
COLD = 0.0
AMBIENT = 25.0
HOT = 50.0
#=========================== USER ADJUSTABLE (end) ===========================

def diffusion(diffusionRate, site, N, NE, E, SE, S, SW, W, NW):
    """Default diffusion function"""

    return(1-8*diffusionRate)*site + diffusionRate*(N + NE + E +  SE + S + SW + W + NW)

def diffusionSto(diffusionRate, site, N, NE, E, SE, S, SW, W, NW):
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
    """ Function to accept a grid of temperatures and to return a grid with heat
    and cold applied at hotSites and coldSites, respectively.
    
    Args:
        bar (matrix):           Matrix of temperatures
        hotSites (list):        List of coordinates of "HOT" cells
        coldSites (list):       List of coordinates of "COLD" cells

    Returns:
        bar (matrix):           Matrix of temps, now + hot and cold cells
        
    """

    newBar = np.copy(bar)

    for coord in hotSites:
        newBar[int(coord[0]), int(coord[1])] = HOT

    for coord in coldSites:
        newBar[int(coord[0]), int(coord[1])] = COLD

    return newBar

def reflectingLat(lat):
    """Function to accept a grid and to return a grid extended one cell in each
    direction with the reflecting boundary conditions.

    Uses numpy.vstack and transpose() to quickly grow the lattice by one row or
    column in each direction, using the current edge as the source.

    Args:
        lat (matrix):           Matrix of temperatures without a boundary

    Returns:
        latNSEW (matrix):       Matrix with a reflecting boundary

    """

    # Stack the first row of lat, lat itself, and the last row of lat
    latNS = np.vstack([lat[0], lat, lat[-1]])

    # tranpose latNS so that the east and west boundaries are now north and
    # south
    latNS = latNS.transpose()
    
    # Repeat the first stacking
    latNS = np.vstack([latNS[0], latNS, latNS[-1]])

    # Re-transpose the lattice back to its original shape
    return latNS.transpose()

def applyDiffusionExtended(latExt, diffusionRate, diffFunc):
    """Function that takes an extended lattice, latExt, and returns the
    internal lattice with diffusion function diffFunc applied to each site.

    Args:
        latExt (matrix):        Lattice extended with reflecting boundaries
        diffusionRate (float):  Rate of diffusion to apply to the Moore
                                neighborhood
        diffFunc (function):    Diffusion function to be used (either default
                                or stochastic in this program)

    """

    intLat = np.copy(latExt)

    for i in range(1,latExt.shape[0]-1):
        for j in range(1,latExt.shape[1]-1):

            # Neighbors start at N (i-1, j) go clockwise to NW (i-1, j-1)
            intLat[i,j] = diffFunc(diffusionRate, latExt[i,j], \
                latExt[i-1, j], latExt[i-1, j+1], latExt[i, j+1], \
                latExt[i+1, j+1], latExt[i+1, j], latExt[i+1, j-1],\
                latExt[i, j-1], latExt[i-1, j-1])

    # Return the internal lattice only (no boundaries)                    
    return intLat[1:-1, 1:-1]

def diffusionSim(m, n, diffusionRate, t, diffFunc = diffusion):
    """Function to return a list of grids in a simulation of the diffusion of
    heat through a metal bar"""

    coldSites = [[m-1, n/3], [m-1, (n/3)+1], [m-1, (n/3)+2], [m-1, (n/3)+3],
            [m-1, (n/3)+4]]
    
    hotSites = [[m/4, 0], [(m/4)+1, 0], [(m/4)+2, 0], [0, n*(3/4)]]
    
    bar = initBar(m, n, hotSites, coldSites)
    grids = np.array([bar], dtype='l')

    for step in range(t):
        barExtended = reflectingLat(bar)
        bar = applyDiffusionExtended( barExtended, diffusionRate,diffFunc)
        bar = applyHotCold(bar, hotSites, coldSites)
        grids = np.append(grids, np.array([bar]), axis=0)

    return grids

if __name__ == "__main__":
    """ Run 100 simulations using a stochastic diffusion method, and track the
    temperature of a given cell over time t for each simulation.  Compare to
    the non-stochastic version.
    
    Do S&S Module 10.2, Project 9. In addition to describing the temperature
    of a designated cell, create two plots, one that shows the mean temperature
    at a given moment in time over the 100 model runs for your stochastic model
    and one that shows the temperature at the same moment in time for the
    non-stochastic model."""

    # Number of steps to simulate
    steps = 20

    # Number of simulation runs
    runs = 10

    # Cell we wish to keep track of [row, col]:
    cell = [5, 14]
    
    # Heat states of the cell above, over 100 simulations
    stoHeats = []
    
    # Run simulation 100 times and record the end heat states for cell
    for i in range(runs):

        # Grab all temperatures across the simulation for desired cell, for
        # plotting later.
        stoHeats.append(diffusionSim(10, 28, 0.1, steps, diffusionSto)[:, cell[0], cell[1]])

    sims = np.array(stoHeats)

    print("Mean end temp for cell, ranges: ", np.mean(sims[:,-1]), 
            (np.amin(sims[:,-1]), np.amax(sims[:,-1])))

    means = np.mean(sims, axis=0)

    # Record a non-stochastic heat simulation for the same cell
    diffHeats = diffusionSim(10, 28, 0.1, steps)[:, cell[0], cell[1]]
    
    # For plotting, include 0th time step + 1st through 'step'th
    times = np.arange(steps+1)

    # Plot the two temp ranges over time
    fig, ax = plt.subplots()

    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.set_xlim([0, steps])
    plt.plot(times, means, label='Stochastic mean')
    plt.plot(times, diffHeats, label='Default diffusion')
    plt.xlabel( "Time steps" )
    plt.ylabel( "Temperature (c)" )
    plt.legend()
    plt.show()

    # From Stack Overflow question:
    # http://stackoverflow.com/questions/17853680/animation-using-matplotlib-with-subplots-and-artistanimation
    fig = plt.figure()
    ax1 = fig.add_subplot(1,1,1)
    ims = []

    output = diffusionSim(10, 28, 0.1, steps, diffusionSto)

    for time in range(output.shape[0]):
        im = ax1.matshow(output[time], cmap=plt.get_cmap('jet'))
        ims.append([im,])     

    #run animation
    ani = animation.ArtistAnimation(fig,ims, interval=100,blit=True)
    #plt.colorbar()
    plt.show()

    # plt.matshow(output[-1], cmap=plt.get_cmap('jet'))
    # plt.matshow(output[-1], cmap=plt.get_cmap('seismic'))
    # plt.colorbar()
    # plt.show()
