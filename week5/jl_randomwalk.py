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
N_TESTS = 100 #- number random walk tests
N_STEPS = 50  #- max. number of random walk steps to see how mean distance
              #  behaves
#=========================== USER ADJUSTABLE (end) ===========================

import time
import numpy as N
import matplotlib.pyplot as plt

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
        line.set_xdata(x_points[:i+1])
        line.set_ydata(y_points[:i+1])
        plt.draw()
        plt.pause(0.5)

    plt.ioff()


def randomWalkDistance(x_points, y_points):
    return N.sqrt(x_points[-1]**2 + y_points[-1]**2)


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
        size = len(tests[i][0])
        
        # Either increment the count of polymers of the current size
        try:
            counts[size] = counts[size] + 1
        # or, if this is the first, set it to 1
        except KeyError as e:
            counts[size] = 1

    return counts

def sawGetLongest(tests, longestSize):

    # Find the first test run dataset that is as long as the
    # longest run found (makes for more interesting plot)
    for test in tests:
        if len(test[0]) == longestSize:
            return test


def meanRandomWalkDistance(n, numTests):
    sumDist = 0.0
    for i in range(numTests):
        xpts, ypts = sawRandomWalkPoints()
        sumDist = sumDist + randomWalkDistance(xpts, ypts)
    return float(sumDist) / numTests


def main():
    # Generate N_TESTS SAW random walks
    runs = []
    for i in range(N_STEPS):
        runs.append(sawRandomWalkPoints())
    
    # Collect information on how many runs hit which lengths
    dict1 = sawCountStepFractions(runs)
    sizes = sorted(dict1.keys())
    counts = sorted(dict1, key=dict1.get)
    print("Step frequencies: ", sizes, counts)

    plt.plot(sizes, counts)
    plt.show()

    # Run a self-avoiding walk Random Walk animation - 
    # no guarantees of length
    xpts, ypts = sawGetLongest(runs, sizes[-1]) #- Test the randomWalkPoints method
    animateWalk(xpts, ypts)            #  using animation

    mean_dist = N.zeros((N_STEPS,), dtype='d')
    for i in range(1,N_STEPS):
        mean_dist[i] = meanRandomWalkDistance(i, N_TESTS)
        print("Mean distance: " + str(mean_dist[i]))

if __name__ == "__main__":
    main()
