# MISR_time_average

This is the grid-based time_averaging module for MISR radiances that is built on a combination of pandas and numpy. Unfortunately, documentation isn't the best at the moment and a lot of the containers and classes are still in testing mode.
Below is an explanation of what the three main python files do and what they are:

geo_grid.py : The main python function that pulls geolocation and geolatitude data\\
misr_tools.py: The python functions that aid in pulling the radiances from the MISR hdf files and setting them to put into the dataframe
grid_block.py: The main file containing the GridBlock class that sets up the grid and the dataframes associated with it. Many of the functions already have documentation with them so you could take a look at that too.

The idea of this grid class is the there is a set of tools that we can use to perform statistical analytics on the misr radiances such that it can be done in self-customized and robust manner. 
