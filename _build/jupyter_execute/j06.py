# basic
import sys
import os

# common
import numpy as np
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from sklearn.cluster import KMeans
import pickle
import warnings
warnings.filterwarnings('ignore')
from IPython.display import Image

#lib
from lib.validation_methodology_plots import *


path_p = r'/home/administrador/Documentos/seasonal/seasonal_forecast/new/'

df_2021 = pd.read_pickle(path_p+'df_coordinates_pmin_sst_mld_2021.pkl')
xs = xr.open_dataset(path_p+'xs_index_vars_19822019_2deg_new.nc')
xds_kma = xr.open_dataset(path_p+'kma_model/xds_kma_index_vars_1b.nc')
xs_dwt_counts = xr.open_dataset(path_p+'kma_model/xds_count_tcs8.nc')
xs_dwt_counts_964 = xr.open_dataset(path_p+'kma_model/xds_count_tcs8_964.nc')
xds_timeM = xr.open_dataset(path_p+'xds_timeM8.nc')
xds_PCA = xr.open_dataset(path_p+'xds_PCA.nc')
xds_kma_ord = xr.open_dataset(path_p+'xds_kma_ord.nc')

<br>
<br>
<br>

#  <font color='navy'>**6. Model Validation** </font> 

>6.1 [Index predictor](#p)<br> <br>
>6.2 [Predictand computation and plotting](#plv)<br> <br><br> <br>













<br>
<br>

**After analizing the tailor-made predictor along the hindcast data for the calibration period (1982-2019), the performace of the model will be validated for year 2020, which has not been included in the predictor calibration process.**

<br> 

<div style="padding: 15px; border: 1px solid transparent; border-color: transparent; margin-bottom: 20px; border-radius: 4px; color: rgb(0,0,0); background-color: #fcf8e3; border-color: #faebcc; ">
    
**Steps:**
<br>  
    
 * **1.** Download and preprocess (file conversion and resolution interpolation) SST and MLD data for the validation time period.
 * **2.** Generation of the index predictor based on the index function obtained at the calibration period.
 * **3.** The fitted Principal Component Analysis for the calibration is used to predict the index principal components in that same temporal-spatial space.
 * **4.** The predicted PCs are assigned to the best match unit group from the fitted K-means clustering -> based on the index predictor a DWT is assigned to each day.
 * **5.** From the DWT the expected mean number of TCs in 3x3º cells map in the target area is known and the monthly aggregated maps are generated.
    
<br>    
 
</div>

<br />
<br />

## <font color='royalblue'>**6.1 Index predictor and DWTs**</font> <a name="p"></a>



<br>

**Download and preprocess (file conversion and resolution interpolation) SST and MLD data for the validation time period.**

path_val = r'/home/administrador/Documentos/seasonal/seasonal_forecast/validation/'
year_val = 2020

change_sst_resolution_val(path_val,year_val)

<br>

**Generation of the index predictor based on the index function obtained at the calibration period.**

xs_val = ds_index_over_time_val(path_val,path_p,year_val)
xs_val

<br>
<br>

**The fitted Principal Component Analysis for the calibration is used to predict the index principal components in that same temporal-spatial space and the predicted PCs are assigned to the best match unit group from the fitted K-means clustering -> based on the index predictor a DWT is assigned to each day.**

val_bmus = PCA_k_means_val(path_p,path_val,xs_val)

<br>
<br>

**Chronology of the DWTs:**

fig_bmus = plot_bmus_chronology(xs_val,val_bmus,year_val)

<br />
<br />

## <font color='royalblue'>**6.2 Predictand computation and plotting**</font> <a name="plv"></a>
<br />

**From the DWT the daily expected mean number of TCs in 8x8º cells map in the target area maps are known and thus the monthly aggregated maps can be computed.**

<br>

**Daily expected number of TCs**

xds_timeline_val,xs_M_val = ds_monthly_probabilities_val(df_2021,val_bmus,xs_val,xs_dwt_counts,xs_dwt_counts_964)

<br>

**Monthly expected number of TCs**

xs_M_val

fig_val_year_8 = plot_validation_year(df_2021,xs_M_val,xds_timeline_val,35)

<br>

**Full season:**

<br>

![TITLE](val.png)

<br> 

<div style="padding: 15px; border: 1px solid transparent; border-color: transparent; margin-bottom: 20px; border-radius: 4px; color: rgb(0,0,0); background-color: #fcf8e3; border-color: #faebcc; ">
    
**The model generally performs well when estimating the expected TC activity and intensity.**
<br>
    
**However rather than reproducing exactly the historical TCs tracks it shows higher number of expected TCs in the TC path and also in the surroundings -> overstimation (January).**
<br>
    
**When a TC is very intense or very close in dates to the previous or following month it leaves its footprint (Harold 1/04 in March).**
   
    
</div>