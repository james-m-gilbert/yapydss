# -*- coding: utf-8 -*-
"""
Created on Tue Jan 22 09:48:45 2019

@author: jmgilbert
"""
import os
import time
ct1 = time.time()
import dss3_functions_reference as dss
import AuxFunctions as af
import datetime as dt
import numpy as np

import pandas as pnd
from io import StringIO


def hecDateParser(datestr):
    # hec datetimes use 2400 as a valid time
    datesplit = datestr.split(':')
    datepart = datesplit[0]
    timepart = datesplit[1]
    daypart = datestr[0:2]
    monpart = datestr[2:5]
    yrpart = datestr[5:9]

    hrpart = int(timepart[0:2])
    if hrpart==24:
        newhrpart='23'
        newdateStr = datepart +':'+ newhrpart + '00'
        pyDate = dt.datetime.strptime(newdateStr,"%d%b%Y:%H%M"  )+dt.timedelta(1/24.) # adding hour back here so that the month/year adjustments happen appropriately
    else:
        pyDate = dt.datetime.strptime(datestr,"%d%b%Y:%H%M"  )
    return(pyDate)
    
#%%
ct2 = time.time()

baseDir = r'C:\Users\jmgilbert\02_Projects\FH2019\folsom-rfro-2019\models\01_calibration\00_InitialReview\American_River_27Apr2012_REVIEW'
dssFile = 'Precipitation_1997_Interp.dss'    
grid_dss_fp = os.path.join(baseDir, dssFile) 

[pl, nrecs, lopnca] = dss.get_catalog(grid_dss_fp)

dssCols = ['ptA', 'ptB', 'ptC', 'ptD', 'ptE', 'ptF'] #'dummy']
dparser = hecDateParser  #lambda date: pnd.datetime.strptime(date,"%d%b%Y:%H%M" )
catDF = pnd.read_table(StringIO('\n'.join(pl)),sep='/',index_col=False,
                       header=None,usecols=[1,2,3,4,5,6], names=dssCols,
                       parse_dates=[3,4], date_parser=dparser)
catDF = catDF.sort_values('ptD',ascending=True)


startDateTime = catDF.iloc[0]['ptD']
#startDateTime = dt.datetime(1996,12, 14, 20,0)
#endDateTime = dt.datetime(1997,1,15, 20,0 )
#endDateTime = dt.datetime(1996,12,14,21,0)
endDateTime = catDF.iloc[0]['ptE']
tdelta = endDateTime - startDateTime
tdeltaHr = tdelta.days*24
thisDTfmt = startDateTime.strftime('%d%b%Y:%H%M').upper()
nextDTfmt = endDateTime.strftime('%d%b%Y:%H%M').upper()

#cpath = r"/SHG/SACRAMENTO/RUNOFF/%s/%s/INTERPOLATED/" %(thisDTfmt, nextDTfmt)
cpath = pl[0]
ret = dss.open_dss(grid_dss_fp)
kdata=None
[headi, nheadi, headc, nheadc, headu, nheadu, data, ndata, lfound] = dss.read_other(ret[0], cpath,kdata)
inthdr = list(headi)

gridInfo = dss.get_gridInfo(inthdr)



#%%
import geopandas as gpd
from shapely.geometry import Polygon


dx = dy = gridInfo['CellSize']  # meters
nCols = gridInfo['nCols']
nRows = gridInfo['nRows']
LLCellX = gridInfo['LLCellX']*dx
LLCellY = gridInfo['LLCellY']*dy
gridType = gridInfo['GridType']

if gridType==420:  #albers SHG
    gridsrs = gridInfo['SpatialRef']
    lat1 = gridsrs['FirstStdParallel']
    lat2 = gridsrs['SecondStdParallel']
    lon0 = gridsrs['CentralMeridian']
    ellps = 'WGS84'  # not sure if this is specified anywhere?
    x0 = gridsrs['FalseEasting']
    y0 = gridsrs['FalseNorthing']
    lat0 = gridsrs['LatitudeProjOrigin']
    p = pyproj.Proj("+proj=aea +lat_1=%.2f +lat_2=%.2f +lat_0=%.2f +lon_0=%.2f +ellps=%s +x_0=%.2f +y_0=%.2f +datum=NAD83 +units=m +no_defs" %(lat1, lat2, lat0, lon0, ellps, x0, y0))
polygons = []

for i in range(nRows):
    for j in range(nCols):
        polygons.append(Polygon([(LLCellX+j*dx,LLCellY+i*dy),   #lower left
                                 (LLCellX+j*dx, LLCellY+(i+1)*dy),  # top left
                                 (LLCellX+(j+1)*dx, LLCellY+(i+1)*dy),  # top right
                                 (LLCellX+(j+1)*dx, LLCellY+(i*dy))]))  # bottom right
        
grid = gpd.GeoDataFrame({'geometry': polygons})
#grid = grid.to_crs(p.srs)
grid.crs = {'proj': p.srs}
grid.to_file(os.path.join(baseDir, 'test_grid.shp'), driver='ESRI Shapefile',
             crs_wkt=p.srs)
#%%
all_precip = np.empty((tdeltaHr,154, 180), dtype=np.float)
ct3 = time.time()
  #26090 
for t in range(tdeltaHr):
    thisDT = startDateTime + dt.timedelta(t/24.)
    nextDT = thisDT + dt.timedelta(1/24.)
    thisDTfmt = thisDT.strftime('%d%b%Y:%H%M').upper()
    nextDTfmt = nextDT.strftime('%d%b%Y:%H%M').upper()
    cpath = r"/SHG/SACRAMENTO/RUNOFF/%s/%s/INTERPOLATED/" %(thisDTfmt, nextDTfmt)
    [headi, nheadi, headc, nheadc, headu, nheadu, data, ndata, lfound] = dss.read_other(ret[0], cpath,kdata)
    inthdr = list(headi)
    all_precip[t,:,:] = dss.grid_decomp(list(data), inthdr[16], 100., 0., 154, 180, returnArray=True)
    
dss.close_dss(ret[0])
ct4 = time.time()

read_dss_time = ct4 -ct3
print("took %s secs to read %i datasets" %(read_dss_time, tdeltaHr))

plt.imshow(np.ma.masked_equal(np.flipud(all_precip[1,:,:].T),0.))
