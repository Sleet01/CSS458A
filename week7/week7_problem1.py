#!/usr/bin/env python3

# problem1.py
# 
# Author: Martin Metke
# Date: 2017/05/08
# For: CSS458A Week 7 Problem1
#
# Numpy re-write of S&S 11.4 Project 1: Cane Toads
#
# Discussion (part 2)
# Based on the below-listed averages, it appears that a cohort of Cane Toads
# will mostly expire over the course of ~19 hours (68,425.2 seconds/3600s/hr)
# but that approximately 10% (3.73 of ~32) will traverse the field given
# ~16 AWPs, 25% of which are fenced.
#
# Running simulation # 100
# Average runtime:                                68425.200000
# Average living toads remaining:                 0.170000
# Average migrated toads:                         3.730000
# Average croaked toads:                          28.060000
#
# Compared to fencing 0% of the AWPs, this is actually a slight
# *reduction* in migration prevention!  One possible explanation is that
# unfenced AWPs near the ingress border can actually attract and halt large
# groups of Cane Toads which then have a difficult time extracting themselves
# from the group before they starve.

# Average runtime:                                68710.680000
# Average living toads remaining:                 0.190000
# Average migrated toads:                         3.530000
# Average croaked toads:                          28.010000
#
# Fencing 50% of water sources does not seem to change the results much:
# Average runtime:                                65444.400000
# Average living toads remaining:                 0.090000
# Average migrated toads:                         3.800000
# Average croaked toads:                          27.950000
# 
# although it does appear that the number of living Cane Toads remaining
# *in* the field is reduced.  It almost looks as though fencing AWPs may
# cause Toads to roam further afield, or there is an error in our logic?
#
# Finally, fencing all AWPs had the following results:
# 
# Average runtime:                                65082.600000
# Average living toads remaining:                 0.110000
# Average migrated toads:                         3.000000
# Average croaked toads:                          28.550000
#
# So it appears that fencing all AWPs did have *some* effect on migration rates,
# but it appears to be a minimal fix compared to the presumed amount of work.
#
# Out of curiousity, I also halved the number of AWPs while leaving fencing
# rate at 25%:
# Average runtime:                                62128.440000
# Average living toads remaining:                 0.140000
# Average migrated toads:                         4.120000
# Average croaked toads:                          27.770000
#
# Astonishingly, this caused the number of migrating toads to *increase*, *and*
# increased the number of surviving (albeit very slightly)
# I would suppose that either: 
#A) reducing available water points causes the toads to range further afield,
#   and they are capable of surviving on the water from their prey long enough
#   to traverse the longer distances between AWPs.
#B) Some suppositions in S&S are incorrect.
#C) My implementation of the S&S algorithms is flawed.
#
# I would probably need to see some literature on actual Cane Toad behavior
# to determine which is the issue.
# - Martin

#============================= IMPORTS =======================================
import numpy as np
import matplotlib.animation as animation
from matplotlib import pyplot as plt
from matplotlib.ticker import MaxNLocator
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
PERCENT_AWP             = 0.010 # Percent of desert cells containing AWPs
PERCENT_AWPS_FENCED     = 0.20  # Can be any float from 0.0 to 1.0
STARVE                  = 0.6   # Internal food level below which toad dies
UNOCCUPIED_VALUE        = 0.0   # Value to set index 2 of unoccupied cells
WATER_HOPPING           = 0.002 # Amount of water toad uses up when hopping
WOULD_LIKE_DRINK        = 0.9   # Internal water level below which toad drinks
WOULD_LIKE_EAT          = 0.9   # Internal water level below which toad eats

#=========================== USER ADJUSTABLE (end) ===========================

class Simulation:
    '''Class that runs a Cane Toad simulation'''

    def __init__(self, interval=24, cycles=2400, plot=True, printout=True):
        '''Constructor/initializer for Simulation.
        
        Args:
            interval (numeric):     Time for simulation to run (hours)
            cycles   (numeric):     Number of cycles for simulation to run
            
        '''
        # Store runtime information
        self.cycles = cycles
        self.interval = interval
        self.plot = plot
        self.printout = printout

        # Calculate dT per cycle based on simulation time interval and cycles
        self.dT = (interval * 3600.0)/cycles

        self.field = Field()
        
        if self.plot:
            self.fig = plt.figure()
            self.ax1 = self.fig.add_subplot(1, 1, 1)


    def run(self):
        '''Runs simulation from start to finish, tracking Cane Toad states via 
        the self.field object.

        Returns:
            snapshots (list):       List of state snapshots detailing Cane Toad
                                    counts over time.

        '''
        # Grab initial state information
        # Snapshot returns animatable figures
        if self.plot:
            snapshots = [self.field.snapshot(self.ax1)]
        
        # report returns a dict of Alive, Migrated, Croaked counts
        statuses = [self.field.report()]

        # Initialize times and current cycle, for later logging
        times = [0]
        cycle = 0

        # Continue running while toads remain and we're not at the cycle limit
        while (not self.field.exterminated() and cycle < self.cycles):

            # Increment cycle
            cycle += 1
            
            # append time stamp
            times.append(cycle * self.dT)
            
            if self.printout:
                print("Running: ", times[-1])

            # run update and record new state information
            statuses.append(self.field.update())

            if self.plot:
                # append animation frame of latest 
                snapshots.append(self.field.snapshot(self.ax1))

            if self.printout:
                print("Counts:", statuses[-1])

        if self.printout:
            print("End time:", times[-1])
            print("End counts:", statuses[-1])
       
        if self.plot:
            ani = animation.ArtistAnimation(self.fig, snapshots, interval = 50,
                    blit=True)
            plt.show()

        return (times, statuses)


class Field:
    def __init__(self, width=42, height=42 ):
        
        self.croakedToads = []
        self.migratedToads = []
        
        self.width = width
        self.height = height

        self.fencedAWPs = []

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

                        # find max of grid or kernel across kernel's area
                        # (we want to merge existing AWPs, not over-write)
                        grid[1,row-2:row+3,col-2:col+3] = np.maximum.reduce( \
                            [ grid[1,row-2:row+3,col-2:col+3], kernel[1] ] )
                    
                        # Decide if it shall be fenced
                        if (np.random.rand() < PERCENT_AWPS_FENCED):

                            self.fencedAWPs.append([col, row])

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


    def update(self):
        '''Main state update function.  Calls Toad consumption and movement
        functions to advance state to next step.

        Returns:
            report  (dict):     Dict of Toad counts
        '''

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
        '''Return information on current toad status.
        
        Returns:
            status (dict):  Dictionary with Alive, Migrated, and Croaked
                            Toad counts.
        '''

        return {"Alive":len(self.aliveToads),
                "Migrated":len(self.migratedToads),
                "Croaked":len(self.croakedToads)}

    def snapshot(self, axis):
        '''Generate an animatable snapshot of the current field state,
        including toads.
        
        Args:
            axis (pyplot axis)  plot.fig.axis component into which to draw
                                the current frame.

        Returns:
            layers (list)       List of artists (layers) for this frame.
                                Will be passed to animation.ArtistAnimation
                                for animated display, if the simulation
                                holding this Field was instantiated with
                                the plot option turned on.
        '''
        toadX = []
        toadY = []

        for toad in self.aliveToads:
            toadX.append(toad.pos[0])
            toadY.append(toad.pos[1])

        fenceX = []
        fenceY = []

        for AWP in self.fencedAWPs:
            fenceX.append(AWP[0])
            fenceY.append(AWP[1])
        
        fieldMap = axis.matshow(self.grid[2])
        fieldFood = axis.matshow(np.clip(self.grid[0], 0,
            FOOD_CELL),cmap='Greys')

        water = np.ma.masked_where(self.grid[1] <= 0, self.grid[1])
        fieldWater = axis.matshow(water)

        fieldFenced = axis.scatter(fenceX, fenceY, c='r', marker='s')
        fieldToads = axis.scatter(toadX, toadY, c='y')

        return [fieldMap, fieldFood, fieldWater, fieldFenced, fieldToads]


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

        # Next, water (exactly like food, but does not decrease resource)
        if(self.water < WOULD_LIKE_DRINK):

            amtDrink = np.amin([AMT_DRINK, 1-self.water, field.grid[1,y,x]])

            if amtDrink <= -1:
                amtDrink = 0

            self.water += amtDrink

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
        hop west
        
        Returns:
            target      (list):         Y, X (Row, Column) offset of target
                                        destination cell
        '''
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
            target      (list):         Y, X (Row, Column) offset of target
                                        destination cell
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
            target      (list):         Y, X (Row, Column) offset of target
                                        destination cell
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
        '''Perform "stay" action; that is, don't move, and use 50% of the
        energy and water used while hopping'''

        self.energy = self.energy - ENERGY_HOPPING / 2.0
        self.water = self.water - WATER_HOPPING / 2.0


    def dessicated(self):
        '''Calculates whether this Toad has dried up to that point that
        it would expire.

        Returns:
            dessicated (bool):      True if dried up, False otherwise
        '''

        return self.water < DESSICATE


    def starved(self):
        '''Calculates whether this Toad has starved to death.

        Returns:
            starved (bool):     True if starved, False otherwise

        '''

        return self.energy < STARVE


    def migrated(self):
        '''Calculates and returns this Toad's migrated state - whether it has
        reached the western edge and can migrate out of the field.
        
        Returns:
            migrated (bool):    True if Toad has reached column 0'''

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


if __name__ == "__main__":

    # Store final results from each sim pass
    # In the form of a tuple containing the end time stamp and
    # final alive/migrated/croaked counts.
    # These will be further refined into separate ndarrays

    results = []
    for i in range(1, 101):
        
        print("Running simulation # %i" % (i,))
        
        sim = Simulation(plot=False, printout=False)
        temp = sim.run()
        results.append((temp[0][-1], temp[1][-1]))

    # Break down results for numpy averaging
    runtimes, alive, migrated, croaked = np.zeros((4, len(results)), dtype='d')
    for j in range(len(results)):
        runtimes[j] = results[j][0]
        alive[j] = results[j][1]["Alive"]
        migrated[j] = results[j][1]["Migrated"]
        croaked[j] = results[j][1]["Croaked"]

    # Print averages over the total number of runs
    print("Average runtime:\t\t\t\t%f" % (np.mean(runtimes)))
    print("Average living toads remaining:\t\t\t%f" % (np.mean(alive)))
    print("Average migrated toads:\t\t\t\t%f" % (np.mean(migrated)))
    print("Average croaked toads:\t\t\t\t%f" % (np.mean(croaked)))

    sim = Simulation(interval=12,cycles=1200, printout=False)
    output = sim.run()
    # After animation is done, collate alive toad counts and do
    # cross-correlation plot.
    for i in range(len(output)):
        alive[i] = results[i][1]["Alive"]

    plt.xcorr(alive, alive)
    plt.show()

