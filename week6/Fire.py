#!/usr/bin/env python3

# Fire.py
#
# Author: Martin Metke
# Date: 2017/05/02
# For:  CSS458A Week 6 Problem2
#
# Evaluation of burn ratio for 17-by-17 forest of trees with various ignition
# probabilities from 10% to 90%, over 5 time steps.
#
# Updated to Python3 compatibility via 2to3 script (from Python 3.6)
#
# Adapted from:
# Introduction to Computational Science:  Modeling and Simulation for the Sciences
# Angela B. Shiflet and George W. Shiflet
# Wofford College
# Copyright 2006 by Princeton University Press
#
# In site,  
# 	EMPTY (0) - empty,  
# 	TREE (1) - non - burning tree,  
# 	BURNING (2) - burning tree  
# Next value based on site and nearest neighbors (N, E, S, W) 
#

import numpy as np
from matplotlib import pyplot as plt
# from graphics import * # graphics uses bad tkinter threading, breaks pyplot
from random import random

EMPTY = 0
TREE = 1
BURNING = 2

WIN_SIZE = 300

    
def main():
    t = 5  # number of time steps
    n = 19  # size of side of total matrix, including borders

    burnProbs = [.1, .2, .3, .4, .5, .6, .7, .8, .9]
    datasets = []

    # Perform a series of runs for each probability of 10%, 20%...90%
    for j in range(len(burnProbs)):
       
        # Store each set of runs in a "dataset" that contains 10 runs of 5
        runs = []

        # Make 10 runs at the current burnProbability
        for k in range(10):
    

            grids = []

            forest = initForest(n)

            grids.append(forest)
            
            for i in range(t):
                forestExtended = extendLat(forest)
                forest = applyExtended(forestExtended, burnProbs[j])
                grids.append(forest)

            runs.append(grids)

        datasets.append(runs)
        
    # Do analysis here
    # Determine average percent burned for each burnProbability
    averages = []
    
    # For each dataset of 10 runs:
    for i in range(len(burnProbs)):
        
        burned = []

        # For each run in 10 runs:
        for j in range(len(datasets[i])):
            # displayMat(datasets[i][j][-1])
            # print()

            # Get the last grid
            gridNDA = np.array(datasets[i][j][-1])
            # print(gridNDA)

            # Count the number of burned squares
            gridBurned = np.where(gridNDA != 1, 1, 0).sum()
            # print( gridBurned )
            
            # Figure the amount burned for this run
            burned.append(gridBurned / ((n -2) ** 2)) 
        
        # print ("Burned [", i,"]: ", burned)
        averages.append(np.mean(burned))

    print("Average burn percentage for each burnProbability :\n", \
            np.multiply(averages, 100))

    #print ("After generation")
    #for dataset in datasets:
    #    for run in dataset:
    #        for grid in run:
    #            displayMat(grid)
    #            print()

    # showGraphs(datasets[0][0])
    # showGraphs(datasets[-1][-1])

    # Use np.polyfit to fit a quadratic to the stochastic points
    c = np.polyfit(np.multiply(burnProbs, 100), np.multiply(averages, 100), 2)

    plt.plot(np.multiply(burnProbs, 100), np.multiply(averages, 100),
    label='C.A. Method')
    plt.plot(np.multiply(burnProbs, 100), np.polyval(c, np.multiply(burnProbs,
        100)), label = 'Quadratic fit')
    plt.xlabel( "Global Burn Probability (%)" )
    plt.ylabel( "Average Burned Trees in 5 steps (%)" )
    plt.legend()
    plt.show()


# Function to return forest of all trees with one burning
# tree in the middle.  Forest is surrounded by ground.

def initForest(n):
    probTree =  1    # probability of grid site occupied by tree
                       # (value 1); i.e., tree density
    probBurning = 0.0  # probability that a tree is burning (value 2);
                       # i.e., fraction of burning trees

    forest = [[] for i in range(n)]

    for i in range(n):
        for j in range(n):
            if random() < probTree:
                if random() < probBurning:
                    forest[i].append(BURNING)
                else:
                    forest[i].append(TREE)
            else:
                forest[i].append(EMPTY)    

    # For S&S 10.3.9: Set the center tree on fire 
    forest[9][9] = (BURNING)

    return forest


# Function to return an (n + 2) - by - (n + 2) matrix
# with periodic boundaries for mat, an n - by - n matrix

def extendLat(mat):
    n = len(mat)
    matNS = [mat[n - 1]]
    matNS = matNS + mat
    matNS.append(mat[0])
    matExt = [[] for i in range(n + 2)]
    for i in range(n + 2):
        matExt[i] = [matNS[i][n - 1]] + matNS[i] + [matNS[i][0]]
    return matExt
        

# Function to display values in a matrix

def displayMat(mat):
    for row in mat:
        print(row)


# Function to apply spread function

def applyExtended(mat, burnProb):
    copy = copyInsideMat(mat)
    n = len(copy)
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            site = mat[i][j]
            N = mat[i - 1][j]
            E = mat[i][j + 1]
            S = mat[i + 1][j]
            W = mat[i][j - 1]
            copy[i - 1][j - 1] = spread(site, N, E, S, W, burnProb) 
    return copy


# Function to return a copy of the inside of a square matrix

def copyInsideMat(mat):
    m = len(mat) - 2
    copy = [[] for i in range(m)]
    
    for i in range(m):
        for j in range(m):
            copy[i].append(mat[i + 1][j + 1])

    return copy


# Function to spread fire by the following rules:
#   At next time step an empty site remains empty.
#   Burning tree results in empty cell next time step.
#   Perhaps next time step tree with burning neighbor(s) burns itself.
#   Perhaps tree is hit by lightning and burns next time step.

def spread(site, N, E, S, W, burnProb = 0.1):
    burnProbability = burnProb     # probability of catching fire - global variable
    if (site == EMPTY) or (site == BURNING):
        returnValue = EMPTY
    elif (site == TREE) and ((N == BURNING) or (E == BURNING) or
                             (S == BURNING) or (W == BURNING)):
        if random() < burnProbability:
            returnValue = BURNING
        else:
            returnValue = TREE
    else:
        returnValue = TREE

    return returnValue


# Function to display animation of a list of grids

def showGraphs(graphList):
    win = GraphWin("Fire", WIN_SIZE, WIN_SIZE)
    win.setBackground("white")
    for grid in graphList:        
        drawMat(win, grid)
 
           

# Function to draw matrix
# Empty (EMPTY = 0) shows yellow; tree (TREE = 1) shows green;
# burning tree (BURNING = 2) shows burnt orange.

def drawMat(win, mat):
    n = len(mat) - 2
    width = WIN_SIZE/(n + 1)
    for j in range(1, n + 1):
        for i in range(1, n + 1):
            cell = Rectangle(Point(width * i, width * j), \
                             Point(width * (i + 1), width * (j + 1)))
            if (mat[i][j] == EMPTY):
                cell.setFill("yellow1")
            elif (mat[i][j] == TREE):
                cell.setFill("green2")
            else:
                cell.setFill("orange2")
            cell.draw(win)


main()
    
