# yapydss: Yet Another Python Wrapper for the HEC-DSS library

The HECLIB library provides a mechanism to interact (read, write) with data
in the US Army Corps of Engineers Hydrologic Engineering Center (HEC) data format
known as HEC-DSS. HECLIB is (historically, at least) written in C, C++, and Fortran
and distributed through shared/dynamic linked libraries. The `yapydss` package
includes some helper functions that wrap the shared library functions to make working
with DSS data in Python a little easier. 

## Some quick history of this package...

I (James) originally developed the code that eventually became the basis for this package
when working with the DSS files associated with CalSim models back in 2017. 
At the time there were no Python libraries that allowed direct access to HECLIB 
functions while being compatible with Python3. 
Since then several (probably better-written) options have become available.
Like the name says, this is yet another option - it has worked well for me and I'm 
making it available in case it's helpful for others.


