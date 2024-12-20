# -*- coding: utf-8 -*-
"""
Created on Wed Nov 14 13:27:55 2018

@author: jmgilbert
"""

import dss3_functions_reference as dss

grid_dss_fp = r'C:\Users\jmgilbert\02_Projects\CalSim_Utilities\Python_Functions\Python_DSS\gridded_data\D_sacdec96_runoff_Copy.dss'
ret = dss.open_dss(grid_dss_fp)
cpath = r"/SHG/SACRAMENTO/RUNOFF/01JAN1997:0000/01JAN1997:0100/INTERPOLATED/"  #01JAN1997:0100

dtyp = dss.get_datatype(ret[0], cpath)

kdata=None
[headi, nheadi, headc, nheadc, headu, nheadu, data, ndata, lfound] = dss.read_other(ret[0], cpath,kdata)
dss.close_dss(ret[0])

data1 = list(data)
inthdr = list(headi)
comphdr = list(headc)
usrhdr = list(headu)




