import sys
import numpy as np
from math import ceil,floor,sqrt
from pyhdf.SD import *


pathname = "/gpfs/largeblockFS/projects/TDataFus/gyzhao/TF/data/MISR/AGP/"
agp_file = "MISR_AM1_AGP_"


def get_latitude_longitude(filename):
	""" 
	Gets MISR agp hdf file and
	outputs the geolatitude and 
	geolongitude datafields in a 
	4-d numpy array
	"""

	hdf = SD(filename)

	lat = hdf.select('GeoLatitude')[:,:,:]

	lon = hdf.select('GeoLongitude')[:,:,:]

	
	array = np.asarray([lat,lon])

	return array

def get_modis_latitude_longitude(modis_filename):
	hdf = SD(modis_filename)
	lat = hdf.select['Latitude']
	lon = hdf.select['Longitude']
	return (lat,lon)

def build_agp_dataset(agp_file,exp):
"""
Takes in MISR agp hdf file 
and grid decimal point number 
and returns a 2 x 180 x 128 x 512 
numpy array that is [longitude, latitude] 
x block x width x height
"""

	#if filetype == 'MISR':
	
	# Obtain coordinate dataset from agp file
	geo_array = get_latitude_longitude(agp_file)

	# Separate into latitude and longitude files 
	# and linearize all blocks into a 1-d array
	lat = geo_array[0].ravel()
	lon = geo_array[1].ravel() 

	# Build a pixel to latitude,longitude map  
	lat_lon = np.squeeze(np.dstack((lon,lat)))

	lat_lon = np.floor(np.float64(lat_lon/exp))*exp
	
	return lat_lon

