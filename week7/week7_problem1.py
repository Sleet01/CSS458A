#!/usr/bin/env python3

# problem1.py
# 
# Author: Martin Metke
# Date: 2017/05/08
# For: CSS458A Week 7 Problem1
#
# Numpy re-write of S&S 11.4 Project 1: Cane Toads
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
AMT_AWP                 = 1     # Water value provided by an AWP point
AMT_AWP_ADS             = 0.4   # Water value 1 block out from AWP
AMT_AWP_OVER2           = 0.2   # Water value 2 blocks out from AWP
AMT_DRINK               = 0.05  # Amount of water a toad can drink in one tick
AMT_EAT                 = 0.01  # Amount of food a toad can eat in one tick
AMT_MIN_INIT            = 0.88  # Minimum initial toad food/water value
DESSICATE               = 0.6   # Internal water level below which toad dies
FOOD_CELL               = 0.05  # Amount of food a given desert cell contains
ENERGY_HOPPING          = 0.002 # Amount of food toad uses up when hopping
FRACTION_WATER          = 0.6   # Ratio of water in food toads consume
INIT_PERCENTAGE_TOADS   = 0.8   # Percent of start cells with toads in tick 0
INIT_RANGE              = 0.12  # Random range added to AMT_MIN_INIT at init
MAY_HOP                 = 0.5   # Chance a toad will hop, barring other needs
PERCENT_AWP             = 0.01  # Percent of desert cells containing AWPs
PERCENT_AWPS_FENCED     = 0.1   # Can be any float from 0.0 to 1.0
STARVE                  = 0.6   # Internal food level below which toad dies
WATER_HOPPING           = 0.002 # Amount of water toad uses up when hopping
WOULD_LIKE_DRINK        = 0.9   # Internal water level below which toad drinks
WOULD_LIKE_EAT          = 0.9   # Internal water level below which toad eats

#=========================== USER ADJUSTABLE (end) ===========================

class Simulation:
    def __init__(self):
        pass

class Field:
    def __init__(self):
        pass

class Toad:
    '''Toad class, simulating the Cane Toad (Bufo marinus)
    '''
    def __init__(self, field, pos):
        '''Constructor/initializer method for Toad class.
        
        Args:
            field (Field)   Instance of Field class that this toad
                            will move across.
            pos (list)      [x, y] position on the field.

        Returns:
            new Toad()
            
        '''

        # Toad will call field methods to sense, move
        self.field = field
        
        # Position within the field
        self.pos = pos

        # Internal state
        self.energy = AMT_MIN_INIT + (np.random.random() * INIT_RANGE)
        self.water = AMT_MIN_INIT + (np.random.random() * INIT_RANGE)


    def senseSurroundings(self):
        '''Gets food, water, and populated values from surroundings by
        grabbing the immediately-surrounding slice of the field's grid
        and selecting the N, E, S, and W chunks only.
        '''
        x, y = self.pos
        adjs = self.field.grid[y-1:y+2, x-1:x+2]
        # Returns sensed values in N, NE, E, SE, S, SW, W, NW order
        return (adjs[:,0,1], adjs[:,0,2], adjs[:,1,2], adjs[:,2,2],
                adjs[:,2,1], adjs[:,2,0], adjs[:,1,0], adjs[:,0,0])


if __name__ == "__main__":


