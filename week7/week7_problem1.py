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
OCCUPIED_VALUE          = 1.0   # Value to set index 2 of a cell when occupied
PERCENT_AWP             = 0.01  # Percent of desert cells containing AWPs
PERCENT_AWPS_FENCED     = 0.25   # Can be any float from 0.0 to 1.0
STARVE                  = 0.6   # Internal food level below which toad dies
UNOCCUPIED_VALUE        = 0.0   # Value to set index 2 of unoccupied cells
WATER_HOPPING           = 0.002 # Amount of water toad uses up when hopping
WOULD_LIKE_DRINK        = 0.9   # Internal water level below which toad drinks
WOULD_LIKE_EAT          = 0.9   # Internal water level below which toad eats

#=========================== USER ADJUSTABLE (end) ===========================

class Simulation:
    '''Class that runs a Cane Toad simulation'''

    def __init__(self, interval=12, cycles=1200):
        '''Constructor/initializer for Simulation.
        
        Args:
            interval (numeric):     Time for simulation to run (hours)
            cycles   (numeric):     Number of cycles for simulation to run
            
        '''
        # Store runtime information
        self.cycles = cycles
        self.interval = interval

        # Calculate dT per cycle based on simulation time interval and cycles
        self.dT = (interval * 3600.0)/cycles
        
        print("Simulation: dT =", self.dT)

        self.numAlive = 0
        self.numCroaked = 0
        self.numMigrated = 0

        self.field = Field()


    def run(self):
        '''Runs simulation from start to finish, tracking Cane Toad states via 
        the self.field object.

        Returns:
            snapshots (list):       List of state snapshots detailing Cane Toad
                                    counts over time.

        '''
        # Grab initial state information
        # Snapshot returns animatable figures
        snapshots = [self.field.snapshot()]
        
        # report returns a dict of Alive, Migrated, Croaked counts
        statuses = [self.field.report()]

        times = [0]
        cycle = 0

        while (not self.field.exterminated() and cycle < self.cycles):

            # Increment cycle
            cycle += 1
            
            # append time stamp
            times.append(cycle * self.dT)
            print("Running: ", times[-1])

            # run update and record new state information
            statuses.append(self.field.update(times[-1]))

            # append animation frame of latest 
            snapshots.append(self.field.snapshot())

            print("Counts:", statuses[-1])

        print("End time:", times[-1])
        print("End counts:", statuses[-1])



class Field:
    def __init__(self, width=42, height=42 ):
        
        self.croakedToads = []
        self.migratedToads = []
        
        self.width = width
        self.height = height

        # Instantiate the grid on which simulation runs
        # Each grid location contains 3 values:
        #   food: the amount of food available on that cell
        #   water: the amount of water in that cell (never runs out)
        #   occupied: tracks whether a cell contains a Toad already
        self.grid = np.zeros((3, width, height), dtype='d')
        self.grid = self.initializeFood(self.grid)
        
        # Initialize AWPs.  Some will be fenced, so their "Occupied" state will
        # also be set.
        self.grid = self.initializeWater(self.grid)
        
        # Add a border around the desert with three -1 food/water walls
        # and one wall of 2 food/water (draws migrating toads away to west)
        self.grid = self.initializeBorders(self.grid)

        # Create toads along the east border of grid; does not actually update
        # grid, though.
        self.aliveToads = self.initializeToads(self.grid)


    def exterminated(self):
        '''Return whether there are any live Toads or not'''

        return len(self.aliveToads) == 0


    def initializeToads(self, grid):

        toadList = []
        col = grid.shape[2]-1
        
        # Can't spawn toads on the top or bottom corner
        for row in range(1,grid.shape[1]-1):

            if (np.random.rand() < INIT_PERCENTAGE_TOADS):

                toadList.append(Toad(self,[col,row]))

        return toadList


    def initializeBorders(self, grid):
        '''Add borders to grid. 
        N, E, S borders are set to [-1, -1, 1]. 
        W border is set to [2, 2, 0].

        Args:
            grid (ndarray):     2D grid of food, water, occupied values

        Returns
            grid (ndarray):     grid with borders

        '''

        # Was: "Create new grid with +2 width and height from grid"
        # Now: just plop the 
        #bgrid = np.zeros((3, grid.shape[1]+2, grid.shape[2]+2), dtype='d')
        # Set North border
        #bgrid[:,0,:] = [-1],[-1], [1]
        grid[:,0,:] = [-1],[-1], [1]
        # Set South border
        #bgrid[:,-1,:] = [-1],[-1], [1]
        grid[:,-1,:] = [-1],[-1], [1]
        # Set East border
        #bgrid[:,:,-1] = [-1],[-1], [1]
        grid[:,:,-1] = [-1],[-1], [1]
        # Set West (emigration) border
        #bgrid[:,:,0] = [2],[2], [0]
        grid[:,:,0] = [2],[2], [0]

        # Insert grid into larger bgrid, leaving borders intact
        
        return grid


    def initializeWater(self, grid):
        '''Add AWPs to grid, add adjacent and 2-over values around them, and
        then fence a random percentage.

        Args:
            grid    (ndarray):  grid to which AWPs will be added

        Returns:
            grid    (ndarray):  modified grid
        '''
        # Kernel for creating AWP sites.
        kernel = np.zeros((3, 5, 5), dtype='d')
        kernel[1,:,:] = AMT_AWP_OVER2
        kernel[1,1:4,1:4] = AMT_AWP_ADS
        kernel[1,2,2] = AMT_AWP

        # Now create fenced AWP kernel by setting the "occupied" value
        # so that toads cannot move into the AWP location, even though they
        # can still sense it.  Only the center is blocked.
        fkernel = np.copy(kernel)
        fkernel[2,2,2] = OCCUPIED_VALUE

        # AWPs cannot be created within 2 cells of the edges or another
        # AWP.
        # Traverse rows in range [2, -2)
        for row in range(2,grid.shape[1] - 2):
            
            # Traverese columns in range [2, -2)
            for col in range(2, grid.shape[2] - 2):
            #for col in range(grid.shape[2] - 4, grid.shape[2] - 2):
                
                # Check if current row, col position already contains a water
                # value (that is, is too close to another AWP.
                if not ( grid[1,row,col] > 0 ):

                    # Decide if we shall generate an AWP here
                    if (np.random.rand() < PERCENT_AWP):

                        print("InitWater: Adding AWP at ", row, col)

                        # find max of grid or kernel across kernel's area
                        # (we want to merge existing AWPs, not over-write)
                        grid[1,row-2:row+3,col-2:col+3] = np.maximum.reduce( \
                            [ grid[1,row-2:row+3,col-2:col+3], kernel[1] ] )
                    
                        # Decide if it shall be fenced
                        if (np.random.rand() < PERCENT_AWPS_FENCED):

                            print("InitWater: Fencing AWP at ", row, col)

                            # find maximum of grid or fkernel's "occupied"
                            # value.  Fenced areas should definitely override
                            # unfenced areas.
                            grid[2,row-2:row+3,col-2:col+3] = np.maximum.reduce( \
                                [ grid[2,row-2:row+3,col-2:col+3], fkernel[2] ] )

        return grid


    def initializeFood(self, grid):
        '''Adds food values to every cell in grid.

        Args:
            grid (ndarray):     2D array of 3 values per cell

        Returns:
            grid (ndarray):     All food values updated to global default

        '''
       
        # Assigns the default FOOD_CELL value to index 0 of each cell
        grid[0,:,:] = FOOD_CELL

        return grid


    def update(self, dT):
        '''Main state update function.  Calls Toad consumption and movement
        functions to advance state to next step.  dT might actually be
        superfluous here.'''

        # Phase 1: consumption
        for toad in self.aliveToads:

            toad.consume()

        # Phase 2: Movement
        for toad in self.aliveToads:

            toad.move()
        
        # Phase 3a: Mark dead and migrated toads
        for toad in self.aliveToads:

            if (toad.dessicated() or toad.starved()):
                self.croakedToads.append(toad)
            elif (toad.migrated()):
                self.migratedToads.append(toad)

        # Phase 3b: remove dead and migrated toads from main list
        for toad in self.croakedToads:
            if (toad in self.aliveToads):
                self.aliveToads.remove(toad)
        for toad in self.migratedToads:
            if (toad in self.aliveToads):
                self.aliveToads.remove(toad)
        
        # Return a report on the current state following updates
        return self.report()


    def report(self):
        '''Return information on current toad status'''

        return {"Alive":len(self.aliveToads),
                "Migrated":len(self.migratedToads),
                "Croaked":len(self.croakedToads)}

    def snapshot(self):
        '''Generate an animatable snapshot of the current field state,
        including toads'''

        return "Click"



class Toad:
    '''Toad class, simulating the Cane Toad (Bufo marinus)
    '''
    def __init__(self, field, pos):
        '''Constructor/initializer method for Toad class.
        
        Args:
            field (Field):  Instance of Field class that this toad
                            will move across.
            pos (list):     [x, y] position on the field.

        Returns:
            new Toad()
            
        '''

        # Toad will call field methods to sense, move
        self.field = field
        
        # Position within the field
        self.pos = pos

        # Mark current cell as occupied
        self.field.grid[2,pos[1], pos[0]] = OCCUPIED_VALUE
        
        # Internal state
        self.energy = AMT_MIN_INIT + (np.random.random() * INIT_RANGE)
        self.water = AMT_MIN_INIT + (np.random.random() * INIT_RANGE)


    def consume(self):
        '''Method by which Toads consume resources from the grid'''
        
        x, y = self.pos
        field = self.field

        # First, deal with food (energy)
        if(self.energy < WOULD_LIKE_EAT):

            # Amount the toad can eat is the smallest of AMT_EAT,
            # the difference between "full" (1) and its current energy,
            # or the total amount of food available at its grid location
            amtEat = np.amin([AMT_EAT, 1-self.energy, field.grid[0,y,x]])
            
            # Account for starting position, which has -1 food
            if amtEat <= -1:
                amtEat = 0

            # Add amtEat to self.energy, and subtract from current grid loc.
            # This amount may be zero
            self.energy += amtEat
            self.field.grid[0,y,x] -= amtEat

            # Calculate how much water was in the food and add to water stores
            # Water cannot exceed 1.0
            self.water += np.amin([1-self.water, (amtEat * FRACTION_WATER)])
            print("CONSUME: Toad consumed %f food at (%i, %i)" % (amtEat, x,
                y))

        # Next, water (exactly like food, but does not decrease resource)
        if(self.water < WOULD_LIKE_DRINK):

            amtDrink = np.amin([AMT_DRINK, 1-self.water, field.grid[1,y,x]])

            if amtDrink <= -1:
                amtDrink = 0

            self.water += amtDrink
            print("CONSUME: Toad consumed %f water at (%i, %i)" % (amtDrink, x,
                y))


        if self.energy > 1.0:
            self.energy = 1.0

        if self.water > 1.0:
            self.water = 1.0


    def move(self):
        '''Method by which Toad determines whether to move and, if so, where to
        move to.'''

        x, y = self.pos
        field = self.field
        surrounds = self.senseSurroundings()
        dy, dx = [0,0]

        # Check if thirsty
        if self.water < WOULD_LIKE_DRINK:
            dy, dx = self.thirsty(surrounds)

        # Otherwise, check if hungry
        elif self.energy < WOULD_LIKE_EAT:
            dy, dx = self.hungry(surrounds)

        elif np.random.rand() < MAY_HOP:
            dy, dx = self.hopForFun()

        # See which target was chosen
        if (dy == 0 and dx == 0):
            self.stay()

        else:
            # See which actual grid cell was chosen
            ty, tx = np.add([y, x], [dy, dx])

            # Make sure the grid is unoccupied and valid
            if (field.grid[ 2, ty, tx] < OCCUPIED_VALUE and \
                field.grid[ 1, ty, tx] > -1 and \
                field.grid[ 0, ty, tx] > -1):
                self.hop(tx, ty)
            else:
                self.stay()

                
    def hop(self, newx, newy):
        '''Actually transfer this Toad's position to another grid cell.

        Pre:                Must have verified that cell is currently empty
        Args:
            newx (int):     X index (column / 3rd index) of new cell
            newy (int):     y index (row / 2nd index) of new cell

        '''
        
        x, y = self.pos
        grid = self.field.grid

        # Set current grid to unoccupied
        grid[2,y,x] = UNOCCUPIED_VALUE

        # Set new grid to occupied
        grid[2,newy,newx] = OCCUPIED_VALUE
        
        # Update my position
        self.pos = [newx, newy]

        # Update energy and water stores
        self.energy -= ENERGY_HOPPING
        self.water -= WATER_HOPPING


    def hopForFun(self):
        '''Choose a random direction in which to hop.  But if on a border,
        hop west'''
        x, y = self.pos
        field = self.field
        cellWater = field.grid[1,y,x]
        target = [0,0]

        # If we're on a border cell and there's an opening to the west, go west
        if (cellWater <= -1.0) and field.grid[2,y,x] < OCCUPIED_VALUE:
            target = [0, -1]
        # But if we're on a border cell and can't go west, stay here.    
        elif (cellWater <= -1.0):
            pass
        # Otherwise, choose a direction to hop to.  
        else:
            # Randomly choose a y and x direction
            choices = [-1, 0, 1]
            np.random.shuffle(choices)
            dy = choices[0]
            np.random.shuffle(choices)
            dx = choices[0]
            target = [dy, dx]
        
        return target
    
        
    def hungry(self, surroundings):
        '''When a Toad is hungry, it chooses a target cell to move to based on
        a hierarchy of needs.
            1) Desire to find more moisture (water > 0 in neighboring cell)
            2) Desire to leave border cell (water = -1)
            3) Desire to conserve water while waiting to leave border cell

        Args:
            surroundings (ndarray):     List of surrounding cells

        Returns:
            target      (index):        Index of cell to go to
        '''
        x, y = self.pos
        field = self.field
        target = [0, 0]
        cellFood = field.grid[0,y,x]
        maxFood = np.amax(surroundings[0])

        # If the current cell has as much food as the next-highest, don't move
        if cellFood >= maxFood:
            pass

        # If we're on a border cell and there's an opening to the west, go west
        elif (cellFood <= -1.0) and field.grid[2,y,x] < OCCUPIED_VALUE:
            target = [0, -1] 

        # Otherwise, if there is a nearby cell with 
        elif (cellFood <= 0.0) and (cellFood > -1.0):
            
            # Find the index/indices of highest nearby food value(s)
            whereMax = np.where(surroundings[1] == np.amax(surroundings[1]))

            # Choose one at random if more than one
            index = np.random.choice(np.arange(len(whereMax[0])))

            target = [whereMax[0][index] -1 , whereMax[1][index] -1]

        
        else:
            pass

        return target


    def thirsty(self, surroundings):
        '''When a Toad is thirsty, it chooses a target cell to move to based on
        a hierarchy of needs.
            1) Desire to stay on an AWP (water == 1)
            2) Desire to find more moisture (water > 0 in neighboring cell)
            3) Desire to leave border cell (water = -1)
            4) Desire to conserve water while waiting to leave border cell

        Args:
            surroundings (ndarray):     List of surrounding cells

        Returns:
            target      (index):        Index of cell to go to
        '''
        x, y = self.pos
        field = self.field
        
        target = [0,0]
        
        cellWater = field.grid[1,y,x]

        # If Toad is on an AWP, it won't move due to water needs (at least)
        if cellWater >= 0.999999999:
            pass
       
        # If we're not on an edge or an AWP/adjacent/2adjacent, move to local
        # max water value
        elif (cellWater <= 0.0 and cellWater > -1.0):
            # Find the index/indices of highest nearby water value(s)
            whereMax = np.where(surroundings[1] == np.amax(surroundings[1]))

            # Choose one at random if more than one
            index = np.random.choice(np.arange(len(whereMax[0])))

            target = [whereMax[0][index] - 1, whereMax[1][index] -1]
        
        # If we're on a border cell and there's an opening to the west, go west
        elif (cellWater <= -1.0) and field.grid[2,y,x-1] < OCCUPIED_VALUE:
            target = [0, -1]

        else:
            pass

        return target


    def stay(self):

        self.energy = self.energy - ENERGY_HOPPING / 2.0
        self.water = self.water - WATER_HOPPING / 2.0


    def dessicated(self):

        return self.water < DESSICATE


    def starved(self):

        return self.energy < STARVE


    def migrated(self):

        return self.pos[0] == 0


    def senseSurroundings(self):
        '''Gets food, water, and populated values from surroundings by
        grabbing the immediately-surrounding slice of the field's grid
        and selecting the N, E, S, and W chunks only.
        '''
        x, y = self.pos
        adjs = np.copy(self.field.grid[:,y-1:y+2, x-1:x+2])
        adjs[:,1,1] = [-2, -2, 2] # Set middle to dummy values
        return adjs
#        try:
#            if(adjs.size == 27):
#                # Returns sensed values in N, NE, E, SE, S, SW, W, NW order
#                return (adjs[:,0,1], adjs[:,0,2], adjs[:,1,2], adjs[:,2,2],
#                        adjs[:,2,1], adjs[:,2,0], adjs[:,1,0], adjs[:,0,0])
#            else: #Should only happen while on the "start" border.
#                # Duplicate current column's values to NE,E,SE readings
#                return (adjs[:,0,1], adjs[:,0,1], adjs[:,1,1],adjs[:,2,1],
#                        adjs[:,2,1], adjs[:,2,0], adjs[:,1,0],adjs[:,0,0])
#        except IndexError as e:
#            print("SENSE: exception %s", e)
#            print("SENSE: Location ( %i, %i)" % (x, y))
#            print("SENSE: Frog", self)
#
#
if __name__ == "__main__":

    sim = []
    sim.append(Simulation())
    sim[0].run()
