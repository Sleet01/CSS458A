#!/usr/bin/env python3

#=======================================================================
#                        General Documentation

"""
"""
#---------------- Module General Import and Declarations ---------------
import numpy as np
import scipy.misc as spm
import math
import time


#-------------------- General Function: exponential -----------------------
def exponential(x, tol=1e-8):
    '''Calculate e^x using a series expansion.

    Calculates an approximation to e^x by summing successive terms of
    (x^n / n!) as n goes from 0 to infinity - to *at least* a tolerance
    that defaults to 1 x 10^-8 unless specified explicitly.
    The partial series will be evaluated to term N where N satisfies the
    bound tol > |(3*x^(N+1)/(N+1)!| (vis Taylor Theorum, with 3 approximating e)

    :param x: exponent to which e will (approximately) be raised
    :param tol: upper bound on error between approximation and e
    :type x: double or float
    :type tol: double or float
    :returns: Taylor approximation of e^x where R() <= tol
    :rtype: double

    :Example:

    >>> In [48]: a = exponential.exponential(3, 1e-8)

    >>> In [49]: a
    >>> Out[49]: 20.085536923187664

    >>> In [50]: a - math.exp(3) <= 1e-8
    >>> Out[50]: True

    .. Note:: this version is a disaster.  Recommend using nexponential instead.
       The accuracy of this approximation will be *at least* as small as
       tolerance tol, but is not guaranteed to be anywhere near tol.  Please
       consider truncating the output if an exact level of tolerance is required.
    '''
    # Cast x to NumPy double.  This avoids some accuracy issues at higher
    # values of x
    x = np.float64(x)

    # Approximate solution to determine N, a number of terms required to meet
    # tolerance tol (although with some margin, as this approximation is...
    # approximate)
    # N1: a good first approximation of the N required to meet tol
    N1 = math.ceil(x*math.log10(3/tol)+math.log10(x))
    # But N must also satisfy log((N+1)!) > N1
    N2 = math.ceil(math.log10(math.factorial(N1)))

    # Should N2 not exceed N1, which is more likely at large tol or large x,
    # increase N2 by the difference between N1 and N2, rounded up.
    # This converges very quickly because log((S!)) increases ~ proportionally
    # to delta-S.
    while (N2 < N1):
        N2 += math.ceil(N1 - math.ceil(math.log10(math.factorial(N2))))

    # Create a 1D array filled with values identical to each term's index
    a = np.arange(N2)

    #Final result is the sum of the partial sequence, represented by a numpy
    #array.
    return np.sum(( x**a ) / spm.factorial(a))

def nexponential(x, tol=1e-8):
    '''Calculate e^x using a naive, iterative series expansion.

    Calculates an approximation to e^x by summing successive terms of
    (x^n / n!) as n goes from 0 to infinity - to *at least* a tolerance
    that defaults to 1 x 10^-8 unless specified explicitly.

    :param x: exponent to which e will (approximately) be raised
    :param tol: upper bound on error between approximation and e
    :type x: double or float
    :type tol: double or float
    :returns: Taylor approximation of e^x where R() <= tol
    :rtype: double

    :Example:

    >>> In [51]: b = exponential.nexponential(3, 1e-8)

    >>> In [52]: b
    >>> Out[52]: 20.085536921517669

    >>> In [53]: b - math.exp(3) <= 1e-8
    >>> Out[53]: True

    '''
    # Cast x to NumPy double.  This avoids some accuracy issues at higher
    # values of x
    x = np.float64(x)

    a = []

    # perform the first pass.
    i = 0
    term = x**i / math.factorial(i)
    a.append(term)

    # Continue adding terms until the last term is as small, or smaller than,
    # tol.  Then sum all terms.
    while (term > tol):
        i += 1
        term = x**i / math.factorial(i)
        a.append(term)

    return np.sum( np.array(a) )


def timeit(func, x, tol):
    '''Simple timer function (not to be confused with timeit.timeit)
    for testing the performance of exponential vs nexponential

    Simply prints the name of the function, and then runs it with the provided
    parameters and prints out the runtime.

    :param func: function name, unquoted.  e.g. e.exponential, e.exponential
    :param x: exponent to which e will (approximately) be raised
    :param tol: upper bound on error between approximation and e
    :type x: double or float
    :type tol: double or float
    :returns: e^x approximation
    :rtype: double

    :Example:

    >>> In [27]: exponential.timeit(exponential.exponential, 1, 1e-5)
    >>> <function exponential at 0x6fffe3d5510>
    >>> 0.0004096031188964844
    >>> Out[27]: 2.7182539682539679

    >>> In [28]: exponential.timeit(exponential.nexponential, 1, 1e-5)
    >>> <function nexponential at 0x6fffda25730>
    >>> 7.724761962890625e-05
    >>> Out[28]: 2.7182815255731918


    '''
    print(str(func))
    start = time.time()
    result = func(x, tol)
    end = time.time()
    print(end - start)
    return result


def testFunctions():
    '''Run basic tests of exponential functions.
    1) Check runtime of exponential() and store results for various X and Tol
    values
    2) Likewise for nexponential()
    '''
    # Test values
    xRange = range(1, 20, 1)
    tRange = [0.1, 0.01, .001, 1e-5, 1e-8, 1e-10]
    results = []
    nresults = []
    expresults = []

    for x in xRange:
        for tol in tRange:
            results.append(timeit(exponential, x, tol))
            nresults.append(timeit(nexponential, x, tol))

            expresults.append(math.exp(x))
            try:
                assert abs(results[-1] - expresults[-1]) <= tol
                assert abs(nresults[-1] - expresults[-1]) <= tol
            except AssertionError as e:
                print(e)
                print("X: ", x, " tol: ", tol)

if __name__ == "__main__":
    testFunctions()
