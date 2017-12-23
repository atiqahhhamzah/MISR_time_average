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
	grid_01 = gb(0.01,shrink=True)
	# #print grid_08.grid


	grid_01.init_geolocation_database()
	grid_01.insert_misr_geolocation(agp_file)
	grid_01.insert_misr_file(misr_file)
	grid_01.save_grid_hdf5('GEO_RAD')




if __name__ == '__main__':
	main()
