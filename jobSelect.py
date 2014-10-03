#
# CDO Operations
# Author:		Robert Sinn
# Last modified: xx xx 2014
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
import operations
import cdoOpps

checkOpp(operation,option,inputFiles,outputFiles,incount = -1,outcount = -1):
	if option == operation:
		if len(inputFiles) != incount and incount != -1
			raise Exception("Insufficent input files")
		if len(outputFiles) != outcount and outcount != -1
			raise Exception("Insufficent output files")
		return 1

	return 0

def jobSelect(opp,inputFiles,outputFiles):
	if opp.startswith('cdo'):
		func = cdoOpps.cdoOpps(opp,inputFiles,outputFiles)
		func(input = inputFiles,output = outputFiles)
		return

	if checkOpp('correlate',opp,inputFiles,outputFiles,2,1):
		func = correlate.run(inputFiles[0],inputFiles[1],outputFiles[0])

	if checkOpp('convolute',opp,inputFiles,outputFiles,2,1):
		func = convolute.run(inputFiles[0],inputFiles[1],outputFiles[0])

def main():
    if len(sys.argv) != 3:
	    error("Operation requires 2 arguments.")
	    return 1 
    return runRegres(sys.argv[1],sys.argv[2])

if __name__ == '__main__':
    exitCode = jobSelect(sys.argv[1],sys.argv[2].split(','),sys.argv[3].split(','))
    exit(exitCode)
