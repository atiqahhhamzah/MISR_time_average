from math import ceil,floor,sqrt
import pandas as pd
import numpy as np
import sys
from pyhdf.SD import *
import geo_grid

shrinked = [64,16]
shrink_tuple = [(180,512,2048),(180,128,512)]

def shrink(data, rows, cols):
"""
	shrink the input data into rowxcols. Row x cols must have a 1:1 aspect ratio with the original row x cols
"""
    return data.reshape(rows, data.shape[0]/rows, cols, data.shape[1]/cols).mean(axis=1).mean(axis=2)

def extract_hdf_radiance(misr_file, shrink_shape=False):
"""
	Extract radiance data from the misr_file given and
	shrink it if shrink_shape is false
"""

	hdf = SD(misr_file)

	# Pull radiance data from the hdf file and put it into a list
	color_band_ds = [hdf.select('Red Radiance/RDQI'),hdf.select('Green Radiance/RDQI'),hdf.select('Blue Radiance/RDQI')]

	# Pull solar zentih data
	solar_zenith = hdf.select('SolarZenith')[:,:,:]

	# Realign width and height if shrink shape is true
	if(shrink_shape == True): 
		expand_val = shrinked[1]
		expand_tuple = shrink_tuple[1]
	else: 
		expand_val = shrinked[0]
		expand_tuple = shrink_tuple[0]

	red = color_band_ds[0][:,:,:]
	green = color_band_ds[1][:,:,:]
	blue = color_band_ds[2][:,:,:]

	# Get rid of the additional 2 bits on the right of the radiance fdata
	red = (np.int16((np.int16(red) >> 2) & 0x3FFF)).astype(np.float_)
	green = (np.int16((np.int16(green) >> 2) & 0x3FFF)).astype(np.float_)
	blue = (np.int16((np.int16(blue) >> 2) & 0x3FFF)).astype(np.float_)


	# Clear out fill data
	red[red >= 16378.0] = np.nan
	green[green >= 16378.0] = np.nan
	blue[blue >= 16378.0]= np.nan

	solarZenith_e = np.zeros(expand_tuple)

	# Expand the solar zenith data into the current width x height and get rid of data > 90
	for i in range(len(solar_zenith)):
		solarZenith_e[i] = np.array(solar_zenith[i].repeat(expand_val,axis=0).repeat(expand_val,axis=1))
		solarZenith_e[i][solarZenith_e[i] >= 90] = -1
		solarZenith_e[i][solarZenith_e[i] < 0] = np.nan

	if(shrink_shape == True):
		red_s = [0]*len(red)
		green_s = [0]*len(red)
		blue_s = [0]*len(red)

		for i in range(len(red)):
			
			red_s[i] = np.array(shrink(red[i],128,512))
			green_s[i] = np.array(shrink(green[i],128,512))
			blue_s[i] = np.array(shrink(blue[i],128,512))

	if(shrink_shape == True): return np.array(([red_s,green_s,blue_s,solarZenith_e]))

	# Return the array of tuples that keep the r, g, b and solar zenith data per pixel
	return np.array([red,green,blue,solarZenith_e])
