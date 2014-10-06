#
# Basic Regression performed by CDO
# Author:		Robert Sinn
# Last modified: 6 Oct 2014
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

import sys
from cdo import *

# Writes an error message to stderr.
def error(message):
    sys.stderr.write("Regression error")
    sys.stderr.write(": ")
    sys.stderr.write(message)
    sys.stderr.write("\n")
    raise Exception("Regression error: " + message)

def runRegress(inputFiles,outputFiles):
    cdo = Cdo()
    cdo.regres(input = inputFiles[0], output = outputFiles[0])
    result = 1

def main():
    if len(sys.argv) != 3:
	    error("Operation requires 2 arguments.")
	    return 1 
    return runRegress(sys.argv[1],sys.argv[2])

if __name__ == '__main__':
    exitCode = main()
    exit(exitCode)
