# -*- coding: utf-8 -*-
"""
Created on Thu Apr 05 15:28:27 2018

@author: jmgilbert
"""

import dss3_functions_reference as dss
import numpy as np

#%%
# open a new dss file
#fp = r'C:/Users/jmgilbert/Desktop/test_write_file.dss'
fp = r'D:\02_Projects\CalSim\util\CalSim_Utilities\Python_Functions\test_write_file3.dss'

ret = dss.open_dss(fp)
#%%
cpath = r"/CALSIM9000/All_The_Water/STORAGE//1MON/9999ZZZ/"
cdate = "31Oct2047"
ctime = "2400"
nvals = 1000
cunits = 'HOGSHEAD'
ctype = 'PER-MAX'
vals = []
for n in range(nvals):
    v = np.random.power(0.667)  #/np.random.beta(0.5, 1.)
    vals.append(v)
    
dss.write_regts(ret[0], cpath, cdate, ctime, nvals, vals, cunits, ctype, 0)

dss.close_dss(ret[0])
#%% test reading the file you just wrote

ret = dss.open_dss(fp)
[nvals, vals2, cunits, ctype, iofset, istat] = dss.read_regts(ret[0], cpath, cdate, ctime, nvals)#.value)
dss.fortran_close_file(71) # does this close the *dsk file?
#plt.plot(vals)  # plot the retrieved time series if you want

dss_diff = []

for n in range(nvals):
    dss_diff.append(vals2[n]-np.float32(vals[n]))
#%%
ret = dss.open_dss(fp)
[nvals, vals3, cunits, ctype, iofset, istat, csupp, coords_info, ctzone, jqual, lfildob, itzone] = dss.read_regtsd(ret[0], cpath, cdate, ctime, nvals, lgetdob_in=True)    
print(coords_info)   
print("ITZONE = %s" %itzone)
dss.close_dss(ret[0])
dss.fortran_close_file(71) # does this close the *dsk file?
#%% test retrieving catalog of new file

# this uses a 'helper' function that tries to execute the following actions, 
#    and, hopefully, will error out with a message any time something doesn't
#    work correctly:
#   1. Open DSS file (prerequisite for creating a catalog)
#       - will create a new empty DSS file if path provided is valid
#   2. Open the catalog if it's available 
#   3. Check if the opened catalog is valid (more checks need to be added though)
#   4. If the catalog is not valid, create a new catalog - assuming both standard
#      and condensed catalogs are wanted
#   5. If records are found in the created catalog, read the path names and...
#   6. return a list of pathnames along with number of records and the flag indicating
#      the open (True) or close (False) status of the catalog file
#
#  syntax: [pathlist, nrecs, lopnca] = dss.get_catalog(fp)  
#         [INPUT]  fp = full file pathname pointing to the DSS file of your choice
#         [OUTPUT] pathlist = list of pathnames
#         [OUTPUT] nrecs = number of records found
#         [OUTPUT] lopnca = flag indicating if the catalog file is closed (it
#                           should be); False = closed, True = open 

[pl, nrecs, lopnca] = dss.get_catalog(fp)

dskfp = r'C:/Users/jmgilbert/02_Projects/CalSim_Utilities/Python_Functions/Python_DSS/test_write_file3.dsk'
with open(dskfp,'ab') as dskf:
    dskf.write('fsa'.encode('utf-8'))


#%%  Testing out reading a gridded dataset stored in DSS
import time
ct1 = time.time()
import dss3_functions_reference as dss
import datetime as dt
ct2 = time.time()
    
grid_dss_fp = r'C:\Users\jmgilbert\02_Projects\CalSim_Utilities\Python_Functions\Python_DSS\gridded_data\D_sacdec96_runoff_Copy.dss'
ret = dss.open_dss(grid_dss_fp)

startDateTime = dt.datetime(1996,12, 14, 20,0)
endDateTime = dt.datetime(1997,1,15, 20,0 )
tdelta = endDateTime - startDateTime
tdeltaHr = tdelta.days*24

all_precip = np.empty((tdeltaHr,154, 180), dtype=np.float)
ct3 = time.time()
kdata=None  #26090 
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
#%%


cpath = r"/SHG/SACRAMENTO/RUNOFF/01JAN1997:0000/01JAN1997:0100/INTERPOLATED/"  #01JAN1997:0100



grid_dss_fp = r'C:\Users\jmgilbert\02_Projects\CalSim_Utilities\Python_Functions\Python_DSS\gridded_data\D_sacdec96_runoff_Copy.dss'
ret = dss.open_dss(grid_dss_fp)
dtyp = dss.get_datatype(ret[0], cpath)

kdata=None  #26090 
[headi, nheadi, headc, nheadc, headu, nheadu, data, ndata, lfound] = dss.read_other(ret[0], cpath,kdata, kheadi=75)

gridInfo = dss.get_gridInfo(headi)

grid=dss.grid_decomp(list(data), gridInfo['CompressedSize'], gridInfo['CompScaleFactor'], gridInfo['CompBase'], gridInfo['nCols'],gridInfo['nRows'], returnArray=True)

dss.close_dss(ret[0])

data1 = list(data)
inthdr = list(headi)
comphdr = list(headc)
usrhdr = list(headu)

#%%
grid = dss.grid_decomp(data1, inthdr[16], 100., 0., 154, 180, returnArray=True)
plt.imshow(np.ma.masked_equal(np.flipud(grid.T),0.))

#%% test out writing a grid to dss

# first create a grid - lets just do random (non-negative values)
testgrid = np.random.beta(1.8,8.3,size=(20,20))*10
plt.matshow(testgrid)
[freq, bins,grph]=plt.hist(testgrid.flatten())

# now compress it according to the standard/default DSS shift-scale-shorten method
[arrayout, sizeout, totalsize] = dss.grid_comp(testgrid, 100., 0., 20, 20)

# check what happens when we set some valeus to 0
testgrid2 = testgrid.copy()
testgrid2[testgrid2<1.5] = 0.
[arrayout2, sizeout2, totalsize2] = dss.grid_comp(testgrid2, 100., 0., 20, 20)
#%%
import struct

def convert_int(intval, numbytes,rettyp):
    thisBytes = (intval).to_bytes(numbytes, byteorder='little', signed=True)
    
    retval = struct.unpack(rettyp, thisBytes)
    return(retval)