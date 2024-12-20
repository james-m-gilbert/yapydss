# -*- coding: utf-8 -*-
"""
Created on Thu Apr 05 15:28:27 2018

@author: jmgilbert
"""

import dss3_functions_reference as dss
import numpy as np

# open a new dss file
#fp = r'C:/Users/jmgilbert/Desktop/test_write_file.dss'
fp = r'C:\Users\jmgilbert\02_Projects\CalSim_Utilities\Python_Functions\Python_DSS\test_write_file3.dss'

ret1 = dss.open_dss(fp)
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
[nvals, vals, cunits, ctype, iofset, istat] = dss.read_regts(ret[0], cpath, cdate, ctime, nvals)#.value)
#plt.plot(vals)  # plot the retrieved time series if you want

#%% Testing catalog creation - still needs work!! use at your own risk - may crash python!

icunit = 12
icunit0 = 0
icdunt = 13 # set to zero to create condensed catalog
inunit = 0 # set to zero to create a new catalog
labrev = False
lsort = True
global lopnca

lopnca = False

#cat_open_ret = dss.open_catalog(fp, icunit, lgenca_in=True, lgencd_in=True)  # opens catalog - should generate a regular and condensed catalog file
[lgenca, lopnca, lcatlg, lgencd, lopncd, lcatcd, nrecs] = dss.open_catalog(fp, icunit, lgenca_in=True, lgencd_in=True)

[lcatcd, nrecs] = dss.create_catalog(ret[0], icunit, icdunt, inunit, '', labrev, lsort) # creates the catalogs in memory - I don't think this actually writes the files yet
[pathlist, lopnca] = dss.read_catalog(lopnca, icunitin=icunit)

dss.fortran_close_file(icunit)  #closes main catalog file 
dss.fortran_close_file(13)    #closes condensed catalog file
dss.fortran_close_file(12)
dss.fortran_close_file(0)
#os.close(0)  #??
dss.close_dss(ret[0])  # close the dss file



#%%
nfp = r'C:\Users\jmgilbert\02_Projects\CalSim_Utilities\Python_Functions\Python_DSS\test_write_file3.dsk'
for n in range(0,160):
    #dss.fortran_close_file(n)
    try:
        #os.remove(nfp)
        os.close(n)
        print("it was file unit %i" %n)
    except:
        pass
    
#%%
        
for proc in psutil.process_iter():
    try:
        # this returns the list of opened files by the current process
        flist = proc.open_files()
        if flist:
            print(proc.pid,proc.name)
            for nt in flist:
                print("\t",nt.path)

    # This catches a race condition where a process ends
    # before we can examine its files    
    except psutil.NoSuchProcess as err:
        print("****",err)
        
        
#%%
        
with open(nfp,'ab') as dskf:
    dskf.write('fsa'.encode('utf-8'))
    