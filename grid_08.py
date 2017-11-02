import pandas as pd
import numpy as np
from grid_block import GridBlock as gb
import sys
import misr_tools
from pyhdf.SD import *

#Set up of grid block with agp files
def main():

	agp_file = sys.argv[1]
	misr_file = sys.argv[2]

	# #Starting grid
	grid_08 = gb(0.01)
	# #print grid_08.grid


	grid_08.init_geolocation_database()

	grid_08.insert_misr_geolocation(agp_file)
	grid_08.insert_misr_file(misr_file)
	print "BEFORE AGGR"
	print grid_08.grid
	grid_08.describe()
	grid_08.save_geolocation_db('MISR_GRID_008_GEO')
	grid_08.save_grid('MISR_GRID_008_RADIANCE')
	# grid_08.save_geolocation_db('MISR_GRID_008_GEO');

	#print grid_08.grid
	#print grid_08.geolocation



if __name__ == '__main__':
	main()
