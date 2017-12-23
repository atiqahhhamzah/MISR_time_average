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
	path_str = '{:03d}'.format(path)
	return agp_file_header + path_str + '.hdf'


def main():

	file_locs = ['']*31
	for i in range(1,32):
		file_locs[i-1] = str(misr_file_header) + str(date(2000,3,i)).replace("-",".") + '/'
		print file_locs[i-1]

	with open('2000_03_AN.txt','w+') as f:
		for directory in file_locs:
			for filename in os.listdir(directory):
    			if filename.find('AN') != -1:
    				f.write(str(os.path.join(directory,filename)) + '\n')
        			# print(os.path.join(directory, filename))
        			continue
        		else:
    				continue

	#grid = 0.01
	#monthgb = gb(grid)

	#monthgb.init_geolocation_database()
	




if __name__ == '__main__':
	main()