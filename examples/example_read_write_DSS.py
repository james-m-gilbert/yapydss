# -*- coding: utf-8 -*-
"""
Created on Fri Feb 15 16:52:52 2019

@author: jmgilbert
"""

import os, sys

# Note: to import the `dss3_functions_reference` [`dss`] file, you can either 
# put this file (example_python_dssRW.2023Nov_COEQWAL.py) in the same directory 
# as your `dss` file, or you can add the location of the `dss` file to your system path.
# I generally  opt for the second option - that way you can have your scripts 
# in your project folders rather than in the `dss` folder
#
# To add the location to your path, modify the following line to match the 
# location of the folder containing the dss3_functions_reference.py file on your machine
#sys.path.append(r'D:\\02_Projects\\CalSim\\util\\CalSim_Utilities\\YAPyDSS\\src')

import yapydss as dss
import numpy as np


# open a file - assume you've set the working directory to the same place
#  as this file
fp = r'test_write_file.dss'

# if file doesn't exist, it will be created upon call to 'open_dss'
[ifltab, istat] = dss.open_dss(fp)   # ifltab is a unique integer key with info about the open dataset - if it gets corrupted, you wont' be able to read/write the open DSS file

# make up some data - could also read in from external file from whatever
# process you want
# in this case - make a list of random numbers 'nvals' long
nvals = 1000
vals = []
for n in range(nvals):
    v = np.random.power(0.667)  
    vals.append(v)
    
# DSS regular time series use implied datetime info - i.e. a beginning
# date/time, number of values, and a regular time step interval is required
# and the date/time for specific value is calculated accordingly
cdate = "31Oct2047"  # start date `cdate` as string, in format "DDMonYYYY"
ctime = "2400"       # start time `ctime` as string, in format "HHMM" where hours go up to 24 because HEC....

# the regular time series interval is defined as part of the record path 
# (7-part identifier for a particular time series); each time series needs a 
# defined path of the form /A-part/B-part/C-part/D-part/E-part/F-part, where
# the convention is to set the D-part to beginning datetime
# stamps for a block of data - when writing regular TS to DSS this can be left blank 
# and the HECLIB library will take care of filling it in appropriately
# Note: the E-part (1MON in this case) sets the regular time interval for the series
#       (can be things like 1DAY, 15MIN, etc - see HEC-DSS documentation for allowable values)
cpath = r"/CALSIM9000/All_The_Water/STORAGE//1MON/9999ZZZ/"

# also need to define units and what an individual value measures in the context
# of the time series (period average, an instantaneous value, a cumulative value over the period, etc)
cunits = 'HOGSHEAD'  # limit 8 characters I believe
ctype = 'PER-MAX'    # implies that values are the maximum per time step


# now we can write the data to the DSS file we've opened
dss.write_regts(ifltab, cpath, cdate, ctime, nvals, vals, cunits, ctype, 0)

# let's close the dSS file
dss.close_dss(ifltab)

# now re-open it and read the data back in
[ifltab, istat] = dss.open_dss(fp)
[nvals, vals2, cunits, ctype, iofset, istat] = dss.read_regts(ifltab, cpath, cdate, ctime, nvals)
dss.close_dss(ifltab)

# Everything so far has been done in single-precision - we can read/write in double precision too
# most CalSim studies tend to write out in double precision

# open a file for double precision writing
fp = r'test_write_file_dbl.dss'
[ifltab, istat] = dss.open_dss(fp)

# writing in double precision - calls a function that allows adding extra 
# metadata
coords = [35.3, -127.2, 0.0]  # you can add in the coordinates of your gage point, for example
icdesc = [5, 11, 1, 5, 0, 0]  # integer codes for the coordinate system, datum, etc defined in coords
csupp = 'This is a test.'    # text supplementary information
ctzone = 'PST'               # a time zone identifier
vals = list(np.random.power(0.667, size=nvals))   # same values generator as before

# write to double precision
dss.write_regtsd(ifltab, cpath, cdate, ctime, vals, cunits, ctype,
                 coords=coords, icdesc=icdesc, csupp=csupp, ctzone=ctzone)

# let's close the dSS file again
dss.close_dss(ifltab)

# ....and re-open it
[ifltab, istat] = dss.open_dss(fp)
[nvals, vals3, cunits, ctype, iofset, istat, \
 csupp, coords_info, ctzone, jqual, lfildob, itzone] = dss.read_regtsd(ifltab, cpath, cdate, ctime, nvals, lgetdob_in=True) 

# and close it out one last time
dss.close_dss(ifltab)
