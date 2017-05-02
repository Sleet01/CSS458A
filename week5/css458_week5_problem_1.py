#=============================================================================
# CSS458 Week 5 Homework - Random walk program
#
# Solution to S&S Module 14.1 a-d, with plots but sans empirical modeling.
#
# By Martin Metke
# April 24, 2017
#
# Notes:
# - Adapted for Python 3.6
# - About animation in matplotlib:
#   http://wiki.scipy.org/Cookbook/Matplotlib/Animations
#   http://matplotlib.org/api/pyplot_api.html#matplotlib.pyplot.plot
#   http://stackoverflow.com/questions/12822762/pylab-ion-in-python-2-
#       matplotlib-1-1-1-and-updating-of-the-plot-while-the-pro
#=============================================================================


#========================== USER ADJUSTABLE (begin) ==========================
N_TESTS = 10000 #- number random walk tests
N_STEPS = 50  #- max. number of random walk steps to see how mean distance
              #  behaves
#=========================== USER ADJUSTABLE (end) ===========================

import time
import numpy as N
import matplotlib.pyplot as plt
import math

def sawRandomWalkPoints():
    """Self-avoiding Random Walk that continues until the "polymer"
    self-intersects."""

    # Start by instantiating a set of X, Y coordinates starting at
    # [0, 0]
    output_list_xy = N.zeros((1,2), dtype='l')

    # Keep generating new points until we hit a previously-passed point
    while(True):

        # Generate a new [[x, y]] point and check if it's in the output list
        # already.
        rand_xy = N.random.randint(2, size=(1,2))
        rand_xy = N.where(rand_xy == 0, -1, 1)

        # Not using cumsum due to having a variable length; just add 
        rand_xy = rand_xy + output_list_xy[-1]

        # Check if rand_xy already exists somewhere in output_list_xy; if so,
        # break out of the while loop
        # avoidHits = N.where(output_list_xy==rand_xy)
        avoidHits = N.where((output_list_xy[:, 0] == rand_xy[0,0]) & \
            (output_list_xy[:, 1] == rand_xy[0,1]))

        if(avoidHits[0].size == 0):
            output_list_xy = N.append(output_list_xy, rand_xy, 0)
        else:
            break

    # Turns the array of coordinates into 2 x 1d arrays of x or y values
    return N.hsplit(output_list_xy, 2)


def animateWalk(x_points, y_points):
    plt.ion()    #- Turn interative mode on

    mylines = plt.plot(x_points, y_points, "o-")  #- mylines is a list of
                                                  #  lines drawn by plot
    line = mylines[0]  #- there's only one line drawn by the above plot call
    plt.axis([N.min(x_points), N.max(x_points), 
              N.min(y_points), N.max(y_points)])

    for i in range(N.size(x_points)):
        # line.set_xdata(x_points[:i+1])
        # line.set_ydata(y_points[:i+1])

        ##### FOR iPython 3 / Python 3.6m compatibility! ######
        # If set_data, or set_xdata/set_ydata, is called while interactive mode
        # is on, pyplot automatically attempts to refresh the plot - even
        # before the y data has been refreshed.  This causes a crash because y
        # data has not been refreshed, which means len(xdata) != len(ydata),
        # which is an invalid state.  So this method of updating a growing data
        # set during interactive mode is no longer workable.
        plt.ioff()
        line.set_data(x_points[:i+1], y_points[:i+1])
        plt.ion()

        # Let the last frame linger
        if (i == N.size(x_points) -1):
            plt.ioff()
            plt.show()
        else:
            plt.draw()
            plt.pause(0.1)


def sawMeanRandomWalkDist(tests):
    
    sumDist = 0.0

    for i in range(len(tests)):
        sumDist = sumDist + randomWalkDistance(tests[0], tests[1])

    return float(sumDist) / len(tests)

def sawCountStepFractions(tests):
    
    # Accumulate all sizes of "polymer" found in the simulation
    # in a dictionary, which we will return
    counts = {}
    
    # Traverse the set of test results
    for i in range(len(tests)):
        # Find how long the current test's polymer was, in steps
        # This is 1 less than the number of points.
        size = len(tests[i][0]) - 1
        
        # Either increment the count of polymers of the current size
        try:
            counts[size] = counts[size] + 1
        # or, if this is the first, set it to 1
        except KeyError as e:
            counts[size] = 1

    # We store each length of run as the keys in 'counts'
    sizes = sorted(counts.keys())
    # The count of runs of each length are stored as the items in 'counts'
    totals = sorted(counts, key=counts.get)

    # We want the fraction of times each specific size makes up, among all the
    # runs.  That is, f(n) == count(runs of size n) / count(all runs)
    # The size n is stored in sizes[i].  The count of runs of that size are
    # stored in totals[i].  The count of all runs is the sum of totals,
    # so we want the element-wise dividend of totals / sum(totals):
    fractions = N.divide(totals, N.sum(totals))

    return (sizes, fractions)

def sawGetLongest(tests, longestSize):

    # Find the first test run dataset that is as long as the
    # longest run found (makes for more interesting plot)
    for test in tests:
        if len(test[0]) == longestSize + 1:
            return test


def rmsDisplacements(tests, sizelist):
    '''Given a set of SAW random walk displacement runs, and the list of sizes
    that have been found in that set, this function returns the Root Mean
    Square Displacement for all runs of size n where n is sizelist[0] through
    sizelist[-1].'''

    # Accumulate rms displacements here
    displacements = []

    for size in sizelist:
        
        count = 0
        curSquares = 0
        
        for test in tests:
            
            # If we find a test run that matches the size we're assessing,
            # increase the count for that size by 1, and 
            # if len(test[0]) == size + 1:
            if len(test[0]) >= size + 1:

                count = count + 1
                curSquares = curSquares + (test[0][-1]**2) + (test[1][-1]**2)
        
        displacements.append(math.sqrt(curSquares/(1.0*count)))

    return displacements    


def main():
    # Generate N_TESTS SAW random walks
    runs = []
    for i in range(N_TESTS):
        runs.append(sawRandomWalkPoints())
    
    # Collect information on how many runs hit which lengths
    (sizes, counts) = sawCountStepFractions(runs)
    print("Step frequencies: ", sizes, counts)

    # Format plot of f(n) vs n steps
    plt.plot(sizes, counts)
    plt.title("Frequency of walk lengths")
    plt.xlabel("Length of Random Walk (Steps)")
    plt.ylabel("Fraction of Length-N Walks")
    plt.axis([N.min(sizes), N.max(sizes), \
             N.min(counts), N.max(counts)])
    plt.show()

    # Run a self-avoiding walk Random Walk animation - 
    # no guarantees of length
    xpts, ypts = sawGetLongest(runs, sizes[-1]) #- Test the randomWalkPoints method
    animateWalk(xpts, ypts)            #  using animation

    rmsds = rmsDisplacements(runs, sizes)
    for i in range(len(rmsds)):
        print ("Average Root Mean Square Displacement for size ", sizes[i], \
            " is ", rmsds[i])
    plt.plot(sizes, rmsds)
    plt.title("Root Mean Square Displacement R for size n")
    plt.xlabel("Length of Random Walk (Steps)")
    plt.ylabel("Root Mean Square Displacement")
    plt.show()


if __name__ == "__main__":
    main()
