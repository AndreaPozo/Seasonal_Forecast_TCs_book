# basic
import sys
import os

# common
import numpy as np
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import pickle

#lib
from lib.plots_base import basemap_ibtracs, basemap_var, basemap_scatter, axplot_basemap, basemap_scatter_both, plot_target_area,plot_predictor_grid
from lib.plots_tcs import get_storm_color, get_category, Plot_DWTs_tracks
from lib.plots_aux import data_to_discret, colors_dwt
from lib.extract_tcs import Extract_Rectangle, dwt_tcs_count
from lib.predictor_definition_building import *

import warnings
warnings.filterwarnings('ignore')
from IPython.display import Image

<br>
<br>
<br>

#  <font color='navy'>**3. Index Predictor Definition and Building** </font> 

>3.1 [Spatial and temporal domain ](#domain) <br> <br>
>3.2 [Predictor grid and data processing](#pg) <br> <br>
>3.3 [Index definition and computation](#dc)<br> <br><br> <br>













## <font color='royalblue'>**3.1 Spatial and temporal domain**</font> <a name="domain"></a>

<br />

**The predictor area spans around the islands of Tonga, Samoa and Fiji, from latitude 0º to 30º and from longitude 160º to 210º; far enough to be able to identify regional as well as local patterns. The calibration period (time domain) is defined from 1982 to 2019.**

# ibtracs v4 dictionary
d_vns = {
    'longitude': 'lon',
    'latitude': 'lat',
    'time': 'time',
    'pressure': 'wmo_pres',}

lo_SP, la_SP = [130,250], [-60,0]

# predictor area
lo_area = [160, 210]
la_area = [-30, 0]

fig_target_area = plot_target_area(rectangle=[lo_area[0], lo_area[1], la_area[0], la_area[1]])

**The variables required for the methodology are downloaded from the databases:**

+ **Predictand**: Tropical cyclones tracks from IBTrACs, for the minimum pressure point.

+ **Predictor**: NOAA 1/4º daily Optimum Interpolation Sea Surface Temperature (SST) and Mixed Layer Depth (MLD) from the NCEP Climate Forecast System Reanalysis (CFSR).



path_st = r'/home/administrador/Documentos/'
xds_ibtracs, xds_SP = storms_sp(path_st)

# ibtracs v4 dictionary
d_vns = {
    'longitude': 'lon',
    'latitude': 'lat',
    'time': 'time',
    'pressure': 'wmo_pres',}

lo_SP, la_SP = [130,250], [-60,0]

# predictor area
lo_area = [160, 210]
la_area = [-30, 0]

# extract rectangle, 772 a 780
TCs_rect_hist_tracks = Extract_Rectangle(xds_SP, lo_area[0], lo_area[1], la_area[0], la_area[1], d_vns) 


df0 = df_pressures(xds_ibtracs)
df0[6000:6010]

#path to your daily mean SST and MLD data
path_sst = r'/media/administrador/SAMSUNG/seasonal_forecast/data/SST/'
path_mld = r'/media/administrador/SAMSUNG/seasonal_forecast/data/CFS/ocnmld/'
path_p = r'/home/administrador/Documentos/seasonal/seasonal_forecast/new/'

**For the calibration period the points with pressure, SST and MLD data in the target area are kept.**

df = df_p_sst_mld(df0,path_sst,path_mld)
df_cali = df.drop(df.index[5184:]) #years of the calibration period

# load data
path_p= r'/home/administrador/Documentos/seasonal/seasonal_forecast/new/'
df = pd.read_pickle(path_p+'df_coordinates_pmin_sst_mld_2019.pkl')
df.tail()

## <font color='royalblue'>**3.2 Predictor grid and data processing**</font> <a name="pg"></a>

<br />


**The historical datasets are interpolated into the a 1/2º grid resolution, defining this way the grid for the predictor in the target area.**


fig_predictor_grid = plot_predictor_grid()

**MLD, SST and pressure data plots:**

plot_sst_mlp_pmin_cali(df)

## <font color='royalblue'>**3.3 Index definition and computation**</font> <a name="dc"></a>

<br />

**The historic datasets are combined into the tailor-made index predictor.It built from the combination of SST-MLD-Pmin of the coordinate dataset previously generated, after being discretized in intervals of 0.5ºC and 5m for the SST and MLD respectively.For simplicity the index will range from 0 to 1 accounting for the Pmin limits of our dataset.**
<br>


# discretization: 0.5ºC (SST), 5m (MLD)
xx,yy,zz = data_to_discret(df['sst'].values, df['mld'].values, 0.5, 5, df['pres'].values, 15, 32, 0, 175, option='min')

# index function
index = zz
fmin, fmax = np.nanmin(zz), np.nanmax(zz)
index_zz = (fmax - index) / (fmax-fmin)

# remove nan
index_zz[np.isnan(index_zz)] = 0

<br>

<div style="padding: 15px; border: 1px solid transparent; border-color: transparent; margin-bottom: 20px; border-radius: 4px; color: rgb(0,0,0); background-color: #fcf8e3; border-color: #faebcc; ">

**The index predictor function:** <br>
    
**index<sub>i</sub> = (P<sub>max</sub> - P<sub>i</sub>) / (P<sub>max</sub> - P<sub>min</sub>)**

<br>

**The index plotted in the MLD-SST space:**

fig_index = plot_index(xx,yy,zz,index_zz)

**Final dataset including all the variable and the index predictor values in the predictor grid.**

xs = ds_index_sst_mld_calibration(path_sst,path_mld,df)

path_slp = r'/media/administrador/SAMSUNG/seasonal_forecast/data/CFS/'
path_pp = r'/home/administrador/Documentos/pratel/'
path_trmm = r'/home/administrador/Documentos/TRMM_daily/'

xs = ds_index_sst_mld_slp_pp_calibration(path_pp,path_slp,xs)

xs_trmm = ds_trmm(path_trmm)