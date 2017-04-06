#!/usr/bin/env python3

#=======================================================================
#                        General Documentation

"""A module to read data from ASFG_Ts.txt and plot it vs Julian day.

The Julian day regime used in this file begins at 1 January 1997, with
the decimal term representing number of seconds since midnight / 86,400.

"""
#---------------- Module General Import and Declarations ---------------
import re
import numpy as np
import numpy.ma as ma
import matplotlib.pyplot as plt
import sys

# Define regex to read values with; named groups allow us to use names like
# variables when retrieving match results.
# Since every group is optional, they will be set to None if they are missing
READ_REGEX = re.compile(r'(?P<jdate>(?P<jday>^\d*)\.(?P<jsecond>\d*))?\s'
                        r'(?P<latitude>-?\d{1,3}\.\d{3})?\s'
                        r'(?P<longitude>-?\d{1,3}\.\d{3})?\s'
                        r'(?P<temp>-?\d{1,3}\.\d{3})?$')


#-------------------- General Function: readmaskplot -----------------------
def readmaskplot(filepath):
    '''Open the specified SHEBA Atmospheric Surface Flux Group temp file,
    process it, and plot the temperature data to the screen and a plot file.
    Temperatures above 0 degrees will be masked.

    Reads temperature data from a SHEBA Atmospheric Surface Flux Group file
    and:

    1. Print temperature mean, median, and standard deviation to the screen
    2. Plot x,y graph of julian day, temp to a file

    :param filepath: relative or absolute path to file that will be read
    :type filepath: string
    :returns: success/failure as boolean
    :rtype: boolean

    :Example:

    .. Note::
    '''

    # Try to open the provided file; return false if not found.
    # try:
    #    f = open(filepath, 'r')
    # except FileNotFoundError:
    #    print("File {} could not be opened!".format(filepath))
    #    return False

    #Create ndarrays to store dates and temperatures.
    dates = np.array([],dtype='f')
    temperatures = np.array([],dtype='f')

    # More python3-Pythonic pattern:
    with open(filepath, 'r') as f:
        for line in f:
            readings = READ_REGEX.search(line)
            # If there are absolutely no matches, it's probably a header.
            # Skip to the next line
            if (readings == None):
                continue
            elif (readings.group('jdate') != None) \
                and (readings.group('temp') != None):
                    dates = np.append(dates, float(readings.group('jdate')))
                    temperatures = np.append(temperatures, \
                            float(readings.group('temp')))

    # Create masked versions of the temp and dates arrays so that only valid
    # entries are used for calculations and plotting.
    # Note: we apply the mask for mtemps to dates to get identically-sized
    # marrays
    mtemps = ma.masked_greater(temperatures, 0.0)
    mdates = ma.array(dates, mask=ma.getmask(mtemps))

    # Print out the mean, median, and stdev
    np.set_printoptions(precision = 6)
    print("Mean temperature of this dataset:    {:.6f}".format(mtemps.mean()))
    print("Median temperature of this dataset:  {:.6f}".format(np.median(mtemps)))
    print("Standard deviation of this dataset:  {:.6f}".format(mtemps.std()))

    # Format plot data
    plt.plot(mdates.compressed(), mtemps.compressed())

    # Format extents of plot region
    axisExtents = []
    axisExtents.append(np.amin(mdates.compressed()))
    axisExtents.append(np.amax(mdates.compressed()))
    axisExtents.append(np.amin(mtemps.compressed() -1.0 ))
    axisExtents.append(np.amax(mtemps.compressed() + 1.0 ))
    plt.axis(axisExtents)

    # Set title/labels
    plt.title("CSS458A - Read, Mask, Plot - Martin Metke - 2017/04/06")
    plt.xlabel('Julian Day (with seconds)')
    plt.ylabel('Temperature')

    # Plot / show
    plt.gcf().set_size_inches(11.5, 8)
    # plt.show()
    plt.savefig('readmaskplot_output.png', dpi=600)

if __name__ == "__main__":
    '''Run as "python readmaskplot.py [path string]"
    to process either the default file, or the file at path string'''

    datafile = ""

    if len(sys.argv) > 1:
        datafile = sys.argv[1]
    else:
        datafile = "./ASFG_Ts.txt"

    sys.exit(readmaskplot(datafile))
