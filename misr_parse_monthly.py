import pandas as pd
import numpy as np
from grid_block import GridBlock as gb
from datetime import date
import sys
import misr_tools
from pyhdf.SD import *

misr_file_header = '/gpfs/largeblockFS/projects/TDataFus/gyzhao/TF/data/MISR/MI1B2E.003/'
agp_file_header = '/gpfs/largeblockFS/projects/TDataFus/gyzhao/TF/data/MISR/AGPHR/MISR_HRLL_P'



def setUpAGPHeader(path):
"""
Returns the full path of the AGP file with the path input
within roger
Input 		- path : desired path for agp file
Output		- directory path in ROGER

"""
	path_str = '{:03d}'.format(path)
	return agp_file_header + path_str + '.hdf'


def main():
"""
Parses through the MISR directory of 2000.03 and returns
all agp files for all AN files in that directory in 
a text file called 2000_03_AN.txt
"""
	file_locs = ['']*31
	# Loops through all days in 2000.03 and make a list of all the folder names for the days
	for i in range(1,32):
		file_locs[i-1] = str(misr_file_header) + str(date(2000,3,i)).replace("-",".") + '/'
		print file_locs[i-1]

	# Go through all the folder names and find the AN files in it and write the
	# corresponding agp filename into the agp text file
	with open('2000_03_AN.txt','w+') as f:
		for directory in file_locs:
			for filename in os.listdir(directory):
    			if filename.find('AN') != -1:
    				f.write(str(os.path.join(directory,filename)) + '\n')
        			continue
        		else:
    				continue




if __name__ == '__main__':
	main()