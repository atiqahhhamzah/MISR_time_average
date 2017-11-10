"""
@author : Nurul Atiqah Hamzah
@email : hamzah3@illinois.edu

Fixes Needed as of week of 8/4/2017:
Adapt to Terra Data Fusion blocks and for 
both MISR and MODIS. Currently works fine
with misr but not MODIS due to resolution
differences between MODIS's geolocation 
attributes and radiance data

Other issues:
Still trying to figure out how to do a 
map projection on basemap with dataframe
radiance data

"""

from math import ceil,floor,sqrt
import pandas as pd
import numpy as np
from pyhdf.SD import *
import geo_grid
import misr_tools

class GridBlock:


    def __init__(self,grid_size,filetype='MISR',shrink=False):
        """
        Initializes and computes the class attributes described
        Input       --  grid_size : Desired length of grid
        Attributes  --  grid_size : Initializer grid length
                    --  exp : number of decimal points in grid
                    --  interval : pixel side length in coordinate degrees
                    --  width : grid width in total pixels
                    --  height : grid height in total pixels
                    --  grid_width : total number of grid columns
                    --  grid_height : total number of grid rows
                    --  grid : pandas dataframe that will hold grid data
                    --  geolocation : pandas dataframa that holds geolocation 
                        data (specific to MISR)
        """
        self.shrink = shrink
        self.grid_size = grid_size
        self.width = int(360/grid_size)
        self.height = int(180/grid_size)
        self.filetype = filetype
        self.geolocation = pd.DataFrame()
        self.grid = pd.DataFrame()
        self.grid['X'] = np.nan
        self.grid['Y'] = np.nan
        self.grid['ij'] = np.nan
        self.grid['Red'] = np.nan
        self.grid['Green'] = np.nan
        self.grid['Blue'] = np.nan
        self.grid['SolarZenith'] = np.nan
        # self.grid['Year'] = np.nan
        # # self.grid['Month'] = np.nan
        # # self.grid['Day'] = np.nan
        if self.filetype == 'MISR':
            self.grid['Path'] = np.nan
           # self.grid['Orbit'] = np.nan
        if self.filetype == 'MODIS':
            self.grid['reflectance_offsets'] = np.nan
            self.grid['radiance_offsets'] = np.nan
            self.grid['reflectance_scales'] = np.nan


    def init_geolocation_database(self):
        """
        Initializes the geolocation dataframe iff MISR
        is the filetype since MISRs geolocation data is
        path specific
        """
        if self.filetype == 'MISR':
            self.geolocation['Path'] = np.nan
            self.geolocation['Latitude'] = np.nan
            self.geolocation['Longitude'] = np.nan
            self.geolocation['ij'] = np.nan


    def save_grid_hdf5(self,filename):
        self.grid.to_hdf(filename.strip() + '.h5','MISR_grid_db', table=True, mode='a')
        print 'Saved to ' + filename.strip() + '.h5'

    def save_grid(self,filename):
        """
        Saves the grid dataframe into a pickle
        file which retains the dataframe structure
        Input       -- filename : desired file name
        Output      -- file in current directory
                       containing dataframe
        """
        self.grid.to_pickle(filename.strip() + '.pkl')
        print 'Saved to ' + filename.strip() + '.pkl'
    

    def load_grid(self,filename):
        """
        Loads the existing grid dataframe
        from another pkl file

        """
        self.grid = pd.read_pickle(filename)

    def save_geolocation_hdf5(self,filename):
        self.geolocation.to_hdf(filename.strip() + '.h5','key_to_store', table=True, mode='a')

    def save_geolocation_db(self,filename):
        """
        Save the geolocation database in the gridblock
        to a pkl file
        """
        self.geolocation.to_pickle(filename.strip() + '.pkl')
    

    def load_geolocation_db(self,filename):
        """
        Load the geolocation database from another pkl file
        into the current grid
        """
        self.geolocation = pd.read_pickle(filename)
        

    def insert_geolocation(self,path,latitude,longitude):
        """
        Load path specific latitude and longitude data
        into the geolocation database

        Input       --  path : path associated to latitude 
                               and longitude data
                    --  latitude : lat array loaded into db
                    --  longitude: lon array loaded into db
        """
        if any(self.geolocation.Path == path) == True:
            print "Geolocation information already in database"
            return
        else:
            ij = np.arange(len(latitude))
            df = pd.DataFrame({ 'Path':pd.Series(path,index=list(range(len(latitude))),dtype='int32'),
                                'Latitude':latitude,
                                'Longitude': longitude ,
                                'ij':ij}) 
            self.geolocation = self.geolocation.append(df)
            return


    def insert_misr_geolocation(self, agp_file):
        #Extract path data from file name:
        path = int(agp_file[agp_file.find('_P') + 2: agp_file.find('_P') + 5])
        if any(self.geolocation.Path == path) == True:
            print "Geolocation information already in database"
            return
        lat_lon_arr = geo_grid.build_agp_dataset(agp_file,self.grid_size)
        print "Inserting geolocation values into database"
        ij = np.arange(len(lat_lon_arr))
        df = pd.DataFrame({ 'Path':     pd.Series(path,index=list(range(len(ij))),dtype='int32'),
                            'Latitude': lat_lon_arr[:,1],
                            'Longitude':lat_lon_arr[:,0],
                            'ij':ij})
        self.geolocation = self.geolocation.append(df)
        print "Geolocation insertion complete"

        

    def describe(self):
        """
        Prints out the attributes of the GridBlock
        Object
        """
        print '\nFile type: ' + self.filetype
        print 'Grid Size in degrees: ' + str(self.grid_size)
        print 'Width: ' + str(self.width) + ' px'
        print 'Height: ' + str(self.height) + ' px'
        print 'Grid Columns: ' + str(list(self.grid.columns.values))
        print 'Current grid count: ' + str(self.grid.shape[0]) + '\n'
    

    def insert_misr_file(self, filename, solar_zenith = np.nan, path = np.nan, orbit = np.nan, year = np.nan, month = np.nan, 
        day = np.nan):
        path = int(filename[filename.find('_P') + 2: filename.find('_P') + 5])
        dataset = self.geolocation.loc[self.geolocation['Path'] == path]
        lat_lon = np.squeeze(dataset.as_matrix(['Latitude','Longitude']))
        lat = lat_lon[:,0]
        lon = lat_lon[:,1]
        print "Extracting MISR data"
        misr_data = misr_tools.extract_hdf_radiance(filename,shrink_shape = self.shrink)
        red = misr_data[0].ravel()
        green = misr_data[1].ravel()
        blue = misr_data[2].ravel()
        solar_zenith = misr_data[3].ravel()
        position = np.array([1]*len(red))
        path_pd = pd.Series(path,index=list(range(len(red))),dtype='int32')
        print "Inserting MISR data"
        dataset = pd.DataFrame({ 'X': lon,
                                'Y': lat,
                            'ij':position,
                            'Red': red,
                            'Green': green,
                            'Blue' : blue,
                            'SolarZenith':solar_zenith,
                            'Path':path_pd})
        print "MISR data insertion complete. Getting rid of Nan values"
        dataset = dataset.dropna(subset=['Red','Green','Blue','SolarZenith'])
        self.grid = self.grid.append(dataset)
        print "MISR data appended to dataset"
        #self.grid.dropna(subset=['red'])


    def insert(self,latitude,longitude, position, red = np.nan, green = np.nan, blue = np.nan, 
        solar_zenith = np.nan, path = np.nan, orbit = np.nan, year = np.nan, month = np.nan, 
        day = np.nan, reflectance_scales = np.nan, reflectance_offsets = np.nan,
        radiance_offsets = np.nan):
        """ 
        Appends dataframe with data passed in
        Make sure to have data be related by row index
        or discrepancies will occur
        Input       --  longitude : longitude of pixel (the x coordinate)
                    --  latitude  : latitude of pixels (the y coordinate)
                    --  red : red intensity value (16-bit) of pixel
                    --  green : green intensity value (16-bit) of pixel
                    --  blue : blue intensity value (16-bit) of pixel
                    --  path : path number of granule data passed in
                    --  orbit : orbit number of granule data passed in
                    --  year : year of granule data passed in
                    --  month : month of granule data passed in
                    --  day : day of granule data (if applicable)
                    --  reflectance_scales : MODIS brf conversion requirement
                    --  reflectance_offsets : MODIS brf conversion requirement
                    --  radiance_scales : MODIS brf conversion requirement

        """
        #grid_array = np.int_(np.ceil(latitude/np.float(self.grid_size)))*np.int_(self.grid_width) + np.int_(np.ceil(longitude/np.float_(self.grid_size)))
        if self.filetype == 'MISR':
            dataset = self.geolocation.loc[self.geolocation['Path'] == path]
            lat_lon = np.squeeze(dataset.as_matrix(['Latitude','Longitude']))
            lat = lat_lon[:,0]
            lon = lat_lon[:,1]
            dataset = pd.DataFrame({ 'X': lon,
                            'Y': lat,
                            'ij':position,
                            'Red': red,
                            'Green': green,
                            'Blue' : blue,
                            'Path':pd.Series(path,index=list(range(len(red))),dtype='float32'),
                            'Orbit':np.nan,
                            'Year': year,
                            'Month': month,
                            'Day': day})
        else: 
            lat = latitude
            lon = longitude
            dataset = pd.DataFrame({ 'X': lon,
                            'Y': lat,
                            'ij':position,
                            'Red': red,
                            'Green': green,
                            'Blue' : blue,
                            'Path':pd.Series(path,index=list(range(len(red))),dtype='float32'),
                            'Orbit':np.nan,
                            'Year': year,
                            'Month': month,
                            'Day': day,
                            'SolarZenith': solar_zenith,
                            'reflectance_offsets': pd.Series(reflectance_offsets,index=list(range(len(red))),dtype='float32'),
                            'radiance_offsets': pd.Series(radiance_offsets,index=list(range(len(red))),dtype='float32'),
                            'reflectance_scales': pd.Series(reflectance_scales, index=list(range(len(red))),dtype='float32')})
        self.grid = self.grid.append(dataset)
      

    def aggr_position(self):
        """
        Do an averaging out by pixel location and path
        """
        self.grid = self.grid.groupby(['ij','Path'],as_index=False).mean()
    

    def aggr_custom (self, items):
        """
        Average by the column items passed as items
        Input:    --    items: A list of strings denoting which columns to group by
        """
        self.grid = self.grid.groupby(items,as_index=False).mean()


    def aggr(self):
        """
        Averages and groups data similar in X, Y columns
        into a single index in the dataframe
        """
        # df.groupby("dummy").agg({"returns": [np.mean, np.sum]})
        self.grid = self.grid.groupby(['X', 'Y']).agg({'Red':np.mean, 'Green': np.mean,'Blue' : np.mean, 'ij': np.sum, 'Path': np.mean}).reset_index()


    def sort(self):
        """
        Sorts the dataframe by the X,Y column
        """
        return self.grid.sort_values(['X', 'Y'])

    def clear_empty(self):
        self.grid = self.grid[(self.grid['Red'] != 0) & (self.grid['Green'] != 0) & (self.grid['Blue'] != 0)]
        return self.grid


    def clear_data(self):
        """
        Clears all the data inside the dataframe
        """
        self.grid = self.grid.drop(self.grid.index[:self.grid.shape[0]])


    def get_latitude_longitude(self):
        """
        Returns a list of all X and Y values
        as a numpy array of total index x 2
        Dim 0 being longitude
        Dim 1 being latitude
        """
        return self.grid.as_matrix(['X','Y'])


    def get_radiance_values(self):
        return self.grid.as_matrix(['Red','Green','Blue'])

    
    def get_grid_data(self,grid_num):
        return self.grid[self.grid['Grid Number'] == grid_num]

