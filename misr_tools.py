from math import ceil,floor,sqrt
import pandas as pd
import numpy as np
from pyhdf.SD import *
import geo_grid

def shrink(data, rows, cols):
    return data.reshape(rows, data.shape[0]/rows, cols, data.shape[1]/cols).mean(axis=1).mean(axis=2)

def extract_hdf_radiance(misr_file):

	hdf = SD(misr_file)
	color_band_ds = [hdf.select('Red Radiance/RDQI'),hdf.select('Green Radiance/RDQI'),hdf.select('Blue Radiance/RDQI')]

	red = color_band_ds[0][:,:,:]
	green = color_band_ds[1][:,:,:]
	blue = color_band_ds[2][:,:,:]

	red_s = [0]*len(red)
	green_s = [0]*len(red)
	blue_s = [0]*len(red)

	for i in range(len(red)):
		
		red_s[i] = np.array(shrink(red[i],128,512))
		green_s[i] = np.array(shrink(green[i],128,512))
		blue_s[i] = np.array(shrink(blue[i],128,512))

		red_s[i][red_s[i] == 65515.0] = np.nan
		green_s[i][green_s[i] == 65515.0] = np.nan
		blue_s[i][blue_s[i] == 65515.0] = np.nan

	return [red_s,green_s,blue_s]
