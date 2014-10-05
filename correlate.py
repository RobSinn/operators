#
# One-dimensional netCDF sample file generator
# Author:		Andrew Dunn
# Last modified: 13 May 2014
#
# This file is part of Climate Analyser.
#
# Climate Analyser is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Climate Analyser is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Climate Analyser.
# If not, see <http://www.gnu.org/licenses/>.
#

from netCDF4 import Dataset
import sys
import numpy

# Handles units such as months and years, which num2date does not do.
def parseTime(timeVar):
    from datetime import timedelta

    # CF Metadata standard defines a year and month as the following.
    year = 365.242198781
    month = year / 12.0

    if timeVar.units.startswith("months since "):
        parts = map(int, timeVar.units[13:].split('-'))
        startyear = parts[0]
        startmonth = parts[1]
        startday = parts[2]

        from datetime import datetime
        start = datetime(startyear, startmonth, startday)

        def month_transform(value):
            return start + timedelta(days=value * month)

        return map(month_transform, timeVar)
    else:
        from netCDF4 import num2date
        return num2date(timeVar[:], timeVar.units)

def intersectTime(timeList1, timeList2, threshold=0.5):
    from datetime import timedelta
    thresholdDelta = timedelta(days=threshold)

    startIndex1 = 0
    startIndex2 = 0

    # smallest actually refers to the largest first index.
    smallest = timeList1[0]
    if timeList1[0] < timeList2[0]:
        smallest = timeList2[0]
        startDay = smallest - thresholdDelta
        while timeList1[startIndex1] < startDay:
            startIndex1 += 1
    else:
        startDay = smallest - thresholdDelta
        while timeList2[startIndex2] < startDay:
            startIndex2 += 1

    endIndex1 = len(timeList1) - 1
    endIndex2 = len(timeList2) - 1

    # refers to smallest last index
    largest = timeList1[-1]
    if timeList1[-1] > timeList2[-1]:
        largest = timeList2[-1]
        lastDay = largest + thresholdDelta
        while timeList1[endIndex1] > lastDay:
            endIndex1 -= 1
    else:
        lastDay = largest + thresholdDelta
        while timeList2[endIndex2] > lastDay:
            endIndex1 -= 2

    # Error.
    if endIndex1 < startIndex1 or endIndex2 < startIndex2:
        error("Time coordinate did not overlap.")
        return ([], [], )

    len1 = endIndex1 - startIndex1 + 1
    len2 = endIndex2 - startIndex2 + 1

    length = min(len1, len2)
    from numpy import arange

    # +1 is safe because lenX/length will always be >=1.
    range1 = map(int, arange(startIndex1, endIndex1 + 1, len1/length))
    range2 = map(int, arange(startIndex2, endIndex2 + 1, len2/length))
    return (range1, range2, )

def getVarName(dataset, name):
    if 'long_name' not in dataset.variables[name].ncattrs():
        return name
    if dataset.variables[name].long_name != "":
        return dataset.variables[name].long_name
    return name

def prepareOutput(output, dataset1D, dataset3D):
    og_lats = dataset3D.variables['lat']
    og_lons = dataset3D.variables['lon']

    output.createDimension('lat', len(og_lats))
    latitudes = output.createVariable('lat', 'f4', ('lat', ))
    latitudes.units = 'degrees north'
    latitudes.long_name = 'Latitude'
    latitudes[:] = og_lats[:]

    output.createDimension('lon', len(og_lons))
    longitudes = output.createVariable('lon', 'f4', ('lon', ))
    longitudes.units = 'degrees east'
    longitudes.long_name = 'Longitude'
    longitudes[:] = og_lons[:]

    values = output.createVariable('correlation', 'f8', ('lat', 'lon', ))
    values.units = 'unitless'

    varA = (set(dataset1D.variables.keys())
            - set(dataset1D.dimensions.keys())).pop()
    varB = (set(dataset3D.variables.keys())
            - set(dataset3D.dimensions.keys())).pop()

    values.long_name = ("Correlation between '" + getVarName(dataset1D, varA)
                        + "' and '" + getVarName(dataset3D, varB) + "'")
    return values


def correlation(dataset1D, dataset3D, output):
    vars1D = set(dataset1D.variables.keys()) - set(dataset1D.dimensions.keys())
    vars3D = set(dataset3D.variables.keys()) - set(dataset3D.dimensions.keys())
    
    if len(vars1D) != 1:
        error("Too many variables in 1D dataset.")

    if len(vars3D) != 1:
        error("Too many variables in 3D dataset.")

    if 'time' not in dataset1D.dimensions:
        error("No time dimension in 1D dataset.")

    if 'time' not in dataset3D.dimensions:
        error("No time dimension in 3D dataset.")

    if 'lat' not in dataset3D.dimensions:
        error("No latitude dimension in 3D dataset.")

    if 'lon' not in dataset3D.dimensions:
        error("No longtitude dimension in 3D dataset.")

    time1D = parseTime(dataset1D.variables["time"])
    time3D = parseTime(dataset3D.variables["time"])

    times = intersectTime(time1D, time3D)

    var1D = dataset1D.variables[vars1D.pop()]
    var3D = dataset3D.variables[vars3D.pop()]
    outputVar = prepareOutput(output, dataset1D, dataset3D)
    
    # Actual operation
    index = numpy.take(var1D[:], times[0])
    for lat in xrange(0, len(dataset3D.variables["lat"])):
        for lon in xrange(0, len(dataset3D.variables["lon"])):
            vals = numpy.take(var3D[:, lat, lon], times[1])

            nones = [i for i, x in enumerate(numpy.ma.getmaskarray(vals)) if x == False]

            val = numpy.corrcoef(numpy.take(index, nones),
                                  numpy.take(vals, nones))
            outputVar[lat, lon] = val
    return 1

# Writes an error message to stderr.
def error(message):
    sys.stderr.write("Correlation error")
    sys.stderr.write(": ")
    sys.stderr.write(message)
    sys.stderr.write("\n")
    raise Exception("Correlation error: " + message)


def run(inputFiles,outputFiles):
    try:
        dataset1D = Dataset(inputFiles[0], 'r', format='NETCDF4')
    except:
        error("Could not open '" + inputFiles[0] + "' for reading.")
        return 1
    try:
        dataset3D = Dataset(inputFiles[1], 'r', format='NETCDF4')
    except:
        error("Could not open '" + inputFiles[1] + "' for reading.")
        return 1
    try:
        output = Dataset(outputFiles[0], 'w', format='NETCDF4')
    except:
        error("Could not open '" + outputFiles[0] + "' for writing.")
        return 1
    result = correlation(dataset1D, dataset3D, output)
    dataset1D.close()
    dataset3D.close()
    output.close()
    return result


def main():
    if len(sys.argv) != 4:
	error("Operation requires 3 arguments.")
	return 1 
    return run(sys.argv[1],sys.argv[2],sys.argv[3])

if __name__ == '__main__':
    exitCode = main()
    exit(exitCode)
