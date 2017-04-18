#=============================================================================
# Monte Carlo model to calculate an area
# Solution to Shiflet & Shiflet (2014)'s Figure 9.2.2 problem (p. 379-380)
# By Johnny Lin
# April 13, 2015
#=============================================================================


import numpy as N
import matplotlib.pyplot as plt


def f(x):
    """Function for Figure 9.2.1.
    """
    return N.sqrt(N.power(N.cos(x),2)+1.0)


def do_one_sim(num_darts, xrange=[0.0,2.0], yrange=[0.0,1.5]):
    """Do one Figure 9.2.2 simulation with num_dart darts.
    """
    rand_x = N.random.uniform(low=xrange[0], high=xrange[1], 
                              size=(num_darts,))
    rand_y = N.random.uniform(low=yrange[0], high=yrange[1], 
                              size=(num_darts,))
    rect_area = (xrange[1] - xrange[0]) * (yrange[1] - yrange[0])

    return N.sum( N.where(rand_y < f(rand_x), 1, 0) ) / \
           float(num_darts) * rect_area


def do_one_set_sims(num_sims=100, num_darts=1000):
    """One set of num_sims Monte Carlo simulations.

    Returns a tuple with the mean and standard deviation of the areas
    calculated by the num_sims set of Monte Carlo simulations.
    """
    areas = N.zeros(num_sims, dtype='f')
    for isim in range(num_sims):
        areas[isim] = do_one_sim(num_darts)
    return (N.mean(areas), N.std(areas))


num_darts = N.array([10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000])
area_est = N.zeros(N.size(num_darts), dtype='f')
std_est = N.zeros(N.size(num_darts), dtype='f')

for i in range(N.size(num_darts)):
    indarts = num_darts[i]
    print( "Darts: " + str(indarts) )

    results = do_one_set_sims(num_darts=indarts)
    print( "Mean, std. dev. of area: " + repr(results) )
    area_est[i] = results[0]
    std_est[i] = results[1]

# plt.plot(num_darts, std_est)
# plt.show()
