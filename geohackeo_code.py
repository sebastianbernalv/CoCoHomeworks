# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 21:03:59 2023

@author: bern
"""

# Checking/setting working directory
import os
os.getcwd()

working_drty = "C:\\UI\\Spring 2023 - Python and Geomorphology\\GeoHackeo"
os.chdir(working_drty)

# Importing libraries
import pandas as pd
import matplotlib.pyplot as plt
import xarray as xr
from pathlib import Path

# Loading data
aquasat_data_filename = Path(".")/"sr_wq_rs_join.csv"
aquasat_data = pd.read_csv(aquasat_data_filename)

# Exploring what data we have
aquasat_data.columns.to_list()

# Dropping all rows with NA values in clorofila-a
clorofila_a_data = aquasat_data.dropna(subset="clorofila-a")

clorofila_a_filename = Path(".")/"clorofila_a_only.csv"
clorofila_a_data.to_csv(clorofila_a_filename)

# Checking what water body has greater number of values
clorofila_a_data["type"].unique()
clorofila_a_data[clorofila_a_data["type"] == "Lake"]["clorofila-a"].describe()
clorofila_a_data[clorofila_a_data["type"] == "Stream"]["clorofila-a"].describe()
clorofila_a_data[clorofila_a_data["type"] == "Estuary"]["clorofila-a"].describe()
clorofila_a_data[clorofila_a_data["type"] == "Facility"]["clorofila-a"].describe()

###############################################################################

# Loading raster files
clorofila_drty   = Path(".")/"rasterData_chlorophyll-a"
temperature_drty = Path(".")/"rasterData_sea_temperature"

os.listdir("./rasterData_chlorophyll-a")


aux = xr.open_dataarray(Path(".")/"rasterData_sea_temperature/MYD28M_2021-12-01_gs_720x360.TIFF", engine="rasterio")
aux.plot()  

aux.rio.crs

# From up to down, and from left to right
y_ext = [90, 20]
x_ext = [-100, -20]
aux.sel(y=slice(y_ext[0], y_ext[1]), x=slice(x_ext[0], x_ext[1])).plot()

# ###############################################################################
# # Using only lakes data
# lakes_data = clorofila_a_data[clorofila_a_data["type"] == "Lake"]
# lakes_data

# # Maine State, USA
# # Latitude:
# # 42° 58′ N to 47° 28′ N
# # Longitude:
# # 66° 57′ W to 71° 5′ W
# lakes_data.columns.to_list()
# tempCalc1 = lakes_data[lakes_data["lat"] > 42.0]
# tempCalc1 = tempCalc1[tempCalc1["lat"] < 47.5]
# tempCalc1 = tempCalc1[tempCalc1["long"] < -66.5]
# tempCalc1 = tempCalc1[tempCalc1["long"] > -71.5]

# # Plotting
# plt.scatter(tempCalc1["long"],
#          tempCalc1["lat"],
#          color="black")
# plt.title("Clorophila-a values - Maine State, USA")
# plt.xlabel("Longitude")
# plt.ylabel("Latitude")
# plt.show()

# tempCalc1
# ###############################################################################

def drty2xr(directory, filetype="tif"):
    directory = str(directory)
    directory = ".//" + directory
    
    files = os.listdir(directory)
    files = [ aux[i] for i in range(0,11) if aux[i][-len(filetype):] == filetype ]
    
    out_xr = xr.open_dataarray(directory+"\\"+files[0], engine="rasterio")
    for file in files:
        if file == files[0]: 
            out_xr = out_xr
        else: 
            temp_xr = xr.open_dataarray(directory+"\\"+file, engine="rasterio")
            out_xr = xr.concat([out_xr, temp_xr], dim='band')
        
    return(out_xr)

aux2 = drty2xr(temperature_drty, filetype="TIFF")

aux2ds = aux2.to_dataset(dim='band')
aux2ds

aux2.plot()
aux2ds.plot()
aux2ds["band"].plot()


aux0 = aux2ds.to_stacked_array("z", sample_dims=["band"])
