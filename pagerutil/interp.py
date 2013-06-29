#!/usr/bin/python

import numpy
from scipy import ndimage
from scipy.interpolate import RectBivariateSpline
from pylab import interp

def extraplinpoint(x,y,xi):
    """
    Extrapolate yi from arrays x,y and point xi using linear interpolation.
    @param x: Array of x values.
    @param y: Array of x values.
    @param xi: Scalar x value - must be less than min(x) or greater than max(x).
    @return: yi, the y value corresponding to xi.
    """
    xmax = max(x)
    xmin = min(x)
    ymax = max(y)
    ymin = min(y)
    if xi <= xmax and xi >= xmin:
        raise Exception,"xi must be outside range of x!"
    dx = (xmax - xmin)/1000.0
    
    #interpolate a point just inside the range
    if xi > xmax:
        xt = xmax - dx
    if xi < xmin:
        xt = xmin + dx
    yt = interp(xt,x,y)

    #Then assume that the point outside the range is linear with respect to x and x+dx
    if xi > xmax:
        m = (ymax - yt)/(xmax - xt)
    else:
        m = (yt - ymin)/(xt - xmax)
    b = yt - m * xt
    yi = m * xi + b
    return yi

def interp2(z,xi,yi,method='linear'):
    """
    Interpolate to find zi from input 2D matrix z at matrix positions xi and yi.

    @param z: A 2D numpy array.
    @param xi: A 1D numpy vector of X positions at which to sample z.
    @param yi: A 1D numpy vector of Y positions at which to sample z.
    @keyword method: String option indicating type of interpolation ['nearest','linear']
    @return: An interpolated 2D numpy array of size(len(yi),len(xi)).
    """
    methods = ['linear','nearest']
    if method not in methods:
        raise Exception,'Only methods %s are implemented.  You passed in %s.' % (str(methods),method)
    if method == 'nearest':
        xr = numpy.kron(numpy.ones((len(yi),1)),xi)
        yr = numpy.kron(numpy.ones((1,len(xi))),yi).reshape(len(yi),len(xi),order='FORTRAN')
        zi = ndimage.map_coordinates(z.squeeze(),[yr,xr],order=0,mode='nearest')
        
    if method == 'linear':
        dims = z.shape
        nrows = dims[0]
        ncols = dims[1]
        xrange = numpy.arange(ncols)
        yrange = numpy.arange(nrows)
        outgrid = RectBivariateSpline(yrange,xrange,z,kx=1,ky=1)
        zi = outgrid(yi,xi)
    
    return zi
