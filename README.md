Introduction
------------

pagerlib is a project to extract the generalizable functionality from the original PAGER code.  This
code includes (so far):
 * io functions, mostly for reading various raster formats, including the ShakeMap grid.xml file.
 * generic utility functions, including color representation, interpolation, text and time functions.

The raster format readers all subclass a Grid object, which has methods for extracting
geo-referencing information, converting between (lat,lon) and (row,col) and vice-versa.  It
also knows how to plot itself into a matplotlib axes object.

pagerio Examples
--------

    >>> esrigrid = esri.EsriGrid('datafile1.flt') #floating point file => Grid object
    >>> shakegrid = shake.ShakeGrid('grid.xml',variable='PGA') #USGS ShakeMap grid.xml file => Grid object of PGA
    >>> geodict = shakegrid.getGeoDict() # return the geo-referencing information from Grid object.
    >>> shakegrid.plot(ax) #plot data into an axes
    >>> row,col = shakegrid.getRowCol(32.34,-119.123) #convert from lat/lon to row/col
    >>> shakegrid.getRowCol(32.34,-119.123) #convert from lat/lon to row/col

A Smattering of pagerutil Examples
--------

    >>> text.commify(123456789) #=> '123,456,789'
    >>> text.floorToNearest(531,100) #=> 500
    >>> text.setNumPrecision(7503445,3) # => 7500000
    >>> timeutil.getTimeElapsedString(datetime(2013,3,1,0,0,0),datetime.now()) => '17 weeks, 0 days'
    >>> z = np.arange(0,16).reshape(4,4) #=> [0,1,2,3;4,5,6,7;8,9,10,11;12,13,14,15] 4x4 array
    >>> xi = np.arange(0.5,2.5,1)
    >>> yi = np.arange(0.5,2.5,1)
    >>> zi = interp.interp2(z,xi,yi) # => [2.5,3.5;6.5,7.5] 2x2 array



