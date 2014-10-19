#
# Basic CDO operations
# Author:		Robert Sinn
# Last modified: 18 10 2014
#
# This file is part of Climate Analyser. This script allows any cdo operator
# to be chosen based on a provided string. Inputs and outputs must also be
# provided
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

def checkOp(option,operation,inputFiles,outputFiles,incount,outcount):
	#Deprecated function. Made avalible if you wish to include file count 
	#checking for cdo operations.
	if option == operation:
		if len(inputFiles) != incount and incount != -1:
			raise Exception("Insufficent input files")
		if len(outputFiles) != outcount and outcount != -1:
			raise Exception("Insufficent output files")
		return 1

	return 0

def cdoCallString(files):
	return ' '.join(map(str, files))

def cdoOps(op,inputFiles,outputFiles):
    	cdo = Cdo()
	func = getattr(cdo, op) #Can't check validity but allows any cdo op
	return func


if __name__ == '__main__':
	func = cdoOps(sys.argv[1],sys.argv[2].split(','),sys.argv[3].split(','))
	func(input = cdoCallString(sys.argv[2].split(',')), output = cdoCallString(sys.argv[3].split(',')))	
	exit()
