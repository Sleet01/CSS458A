#!/usr/bin/env python3

# Author: Martin L. Metke
# Class: CSS 458
# Date: 2017/04/13
# Module 5.7 version of Module 2.2 Excercise 8.a-.d
# A System Dynamics model for Module 2.2 Exercise 8: calculating
# continuous growth of an investment of $500 over 10, 20, 30, or
# 40 years at 9.3% annual continuous growth.

'''This module compares the system dynamics model of continuous compound
interest to the analytically-derived value given by P*e^(r*t), and plots
the output. Accuracy is directly affected by DT (timestep) settings, which
can be adjusted by commenting in/out one of several presets.

Examples:

    c:\>python module5_7_ex_7.py

    c:\>ipython -i module5_7_ex7.py

    c:\>ipython
    In [1]: import module5_7_ex_7
    In [2]: result = module5_7_ex_7.calcInvestmentError(15, 0.034, 1000)
    t               Balance         Analytic Balance                Abs Err                  Rel Error
          0.00           1000.00         1000.00            0.000000e+00            0.000000e+00
          1.00           1034.58         1034.58            6.821678e-05            6.593639e-08
          2.00           1070.37         1070.37            1.411521e-04            1.318728e-07
          3.00           1107.38         1107.38            2.190506e-04            1.978092e-07
          4.00           1145.68         1145.68            3.021685e-04            2.637456e-07
          5.00           1185.30         1185.30            3.907736e-04            3.296819e-07
          6.00           1226.30         1226.30            4.851460e-04            3.956183e-07
          7.00           1268.71         1268.71            5.855787e-04            4.615547e-07
          8.00           1312.59         1312.59            6.923779e-04            5.274911e-07
          9.00           1357.98         1357.98            8.058639e-04            5.934274e-07
         10.00           1404.95         1404.95            9.263716e-04            6.593638e-07
         11.00           1453.54         1453.54            1.054251e-03            7.253002e-07
         12.00           1503.81         1503.81            1.189867e-03            7.912365e-07
         13.00           1555.81         1555.82            1.333603e-03            8.571729e-07
         14.00           1609.62         1609.62            1.485858e-03            9.231092e-07
         15.00           1665.29         1665.29            1.647049e-03            9.890455e-07
    

'''

# imports
import math
import numpy as np
import matplotlib.pyplot as plt

# Set of values to compute against
RUNTIMEVALS = [[10, 0.093, 500], \
               [20, 0.093, 500], \
               [30, 0.093, 500], \
               [40, 0.093, 500]]

# calcInvestmentError function
def calcInvestmentError( simLength, rate, initAmount):
    '''calcInvestmentError determines the compound interest accrued 
    on a given amount at a given rate, and compares the SD estimate
    to the analytically-derived value.

    Args:
        simLength (int, float):     Number of years to run the sim.
        rate (float):               Interest rate as decimal 
                                    (e.g. 1% = 0.01)
        initAmount (int, float):    Starting balance

    Returns:
        list:   A list of Numpy ndarrays, comprising:
                0: timestamps
                1: SD-calculated balance at same-index timestamp
                2: Analytically-calculated balance at same timestamp
                3: Absolute error between 1 and 2 at same timestamp
                4: Relative error between 1 and 2 at same timestamp

    
    '''

    # One tick per hour
    DT = 1 / (365.25 * 24)
    # One tick per month
    # DT = 1 / 12
    # One tick per year
    # DT = 1 / 1
    numIterations = int(simLength / DT) + 1
    print("t\t\tBalance\t\tAnalytic Balance\t\tAbs Err \t\t Rel Error")
    
    # Initialization
    start = 0
    startIteration = 0
    t = 0
    timeList = np.zeros(numIterations, dtype='d')
    balanceList = np.zeros(numIterations, dtype='d')
    balanceList[0] = initAmount

    # Create comparison list of analytically-derived values for each time step
    analyticList = np.arange(0, numIterations*DT, DT, dtype='d')
    analyticList = initAmount * np.exp(rate * analyticList)

    absErrorList = np.zeros(numIterations, dtype='d')
    relErrorList = np.zeros(numIterations, dtype='d')

    # Print initial values
    print ('%10.2f\t%12.2f\t%12.2f\t\t%e\t\t%e' % \
        (t, balanceList[0], analyticList[0], absErrorList[0], relErrorList[0]))

    for i in range(1, numIterations):
        t = i * DT
        timeList[i] = t

        newBalance = balanceList[i-1] + balanceList[i-1]*(rate*DT)
        balanceList[i] = newBalance

        absErrorList[i] = abs(analyticList[i] - balanceList[i])
        relErrorList[i] = abs(analyticList[i] - balanceList[i]) / \
             abs(analyticList[i])

        if ( t % 1 == 0):
            print ('%10.2f\t%12.2f\t%12.2f\t\t%e\t\t%e' % \
                (t, balanceList[i], analyticList[i], absErrorList[i], \
                    relErrorList[i] ))
    
    return [timeList, balanceList, analyticList, absErrorList, relErrorList]

# Main function (runs several passes and plots graph of balances)
def main():
    '''Function run when this module is called as an argument to 
    python[3[.X]], or as an executable, on the command line.
    Runs through four sets of test values, printing the results, and
    finally plots the SD values and Analytical values vs time.
    '''

    resultsList = []
    for val in RUNTIMEVALS:
        resultsList.append(calcInvestmentError(*val))

    plt.plot(resultsList[-1][0], resultsList[-1][1], label='SD method')
    plt.plot(resultsList[-1][0], resultsList[-1][2], 'r--', label='Analytical')
    plt.axis([resultsList[-1][0][0], resultsList[-1][0][-1], \
             0, resultsList[-1][2][-1] + 1000 ])
    plt.xlabel( "Time (Yrs)" )
    plt.ylabel = ( "Balance ($)" )
    plt.legend()
    plt.title( \
        "Comparison of SD to Analytical Calculation of Compound Interest")
    plt.show()

if __name__ == "__main__":
    main()
