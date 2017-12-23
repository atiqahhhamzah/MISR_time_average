import sys
import misr_tools
import numpy as np
from grid_block import GridBlock as gb
from datetime import date
from pyhdf.SD import *

misr_file_header = '/gpfs/largeblockFS/projects/TDataFus/gyzhao/TF/data/MISR/MI1B2E.003/'
agp_file_header = '/gpfs/largeblockFS/projects/TDataFus/gyzhao/TF/data/MISR/AGPHR/MISR_HRLL_P'
cache_file = '2000_03_AN.txt'

def setUpAGPHeader(path):
	"""
	return the AGP filename for the input path
	"""
	path_str = '{:03d}'.format(path)
	return agp_file_header + path_str + '.hdf'

def getMISRPath(filename):
	"""
	extract the path from the filename that is input
	"""
	path = int(filename[filename.find('_P') + 2: filename.find('_P') + 5])
	return path

def main():
	"""
	This is a wrapper function for a misr grid block dataframe
	for one month (2000.03) that will parse through the text file
	produced by misr_parse_monthly.py and build the dataframe
	"""
	saved_geo_fname = "MISR_HRLL_2003.01"
	saved_file_fname = "MISR_TIME_AVG_2003.01"
	agp_cached = dict()

	#Create the grid block for 0.01 degrees and set
	# up the agp dataframe
	grid_01 = gb(0.01)
	grid_01.init_geolocation_database()

	with open(cache_file, 'r') as f:
		for line in f:
			misr_file = line.splitlines()[0]
			path = getMISRPath(misr_file)
			if path in agp_cached:
				agp_cached[path] = True
			else:
				agp_cached[path] = True
				agp_file = setUpAGPHeader(path)
				print >>sys.stderr, "INSERTING MISR HR PATH %d INTO DATABASE ON FILE %s" %(path, agp_file)
				grid_01.insert_misr_geolocation(agp_file)
			print >>sys.stderr, "INSERTING %s" %misr_file
			# insert the misr radiance data into the grid block
			grid_01.insert_misr_file(misr_file)
		f.close()

	print >>sys.stderr, "2003.01 INSERTION COMPLETE. STARTING AGGREGATION"
	grid_01.aggr()
	print >>sys.stderr, "2003.01 AGGREGATION COMPLETE."

	# Save the pandas dataframe as a hdf5 file
	grid_01.save_geolocation_hdf5(saved_geo_fname)
	grid_01.save_grid_hdf5(saved_file_fname)


			

if __name__ == '__main__':
	main()