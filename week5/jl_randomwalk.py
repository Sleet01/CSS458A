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

    return N.hsplit(output_list_xy, 2)


def randomWalkPoints(n):
    output_list_x = N.zeros((n,), dtype='l')
    output_list_y = N.zeros((n,), dtype='l')

    rand = N.random.randint(2, size=(n-1,))
    output_list_x[1:] = N.where(rand == 0, 1, -1)[:]
    output_list_x = N.cumsum(output_list_x)

    rand = N.random.randint(2, size=(n-1,))
    output_list_y[1:] = N.where(rand == 0, 1, -1)[:]
    output_list_y = N.cumsum(output_list_y)

    return (output_list_x, output_list_y)


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


def randomWalkDistance(x_points, y_points):
    return N.sqrt(x_points[-1]**2 + y_points[-1]**2)


def meanRandomWalkDistance(n, numTests):
    sumDist = 0.0
    for i in range(numTests):
        xpts, ypts = randomWalkPoints(n)
        sumDist = sumDist + randomWalkDistance(xpts, ypts)
    return float(sumDist) / numTests

def main():
    # xpts, ypts = randomWalkPoints(35)   #- Test the randomWalkPoints method
    xpts, ypts = sawRandomWalkPoints()   #- Test the randomWalkPoints method
    animateWalk(xpts, ypts)            #  using animation

    mean_dist = N.zeros((N_STEPS,), dtype='d')
    for i in range(1,N_STEPS):
        mean_dist[i] = meanRandomWalkDistance(i, N_TESTS)
        print("Mean distance: " + str(mean_dist[i]))

    plt.figure(2)
    plt.plot(N.arange(N_STEPS), mean_dist, 'o')
    plt.show()

if __name__ == "__main__":
    main()
