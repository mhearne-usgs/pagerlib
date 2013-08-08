#!/usr/bin/env python

#stdlib imports
import sys

#third party libraries
import gdal
import osr
from gdalconst import *
import numpy

#local imports
from grid import Grid

class TiffGrid(Grid):
    """
    Create Grid object from GeoTiff file.
    """
    
    def __init__(self,grdfile=None):
        """
        Create Grid object from GeoTiff file.

        @param grdfile: Valid path to geotiff file.
        """
        self.geodict = {}
        if grdfile is None:
            return
        ds = gdal.Open(grdfile, GA_ReadOnly)
        if ds is None:
            print 'Could not open ' + fn
            sys.exit(1)
        ncols = ds.RasterXSize
        nrows = ds.RasterYSize
        nbands = ds.RasterCount
        self.griddata = numpy.zeros((nrows,ncols,nbands))
        geotransform = ds.GetGeoTransform()
        ulx = geotransform[0]
        uly = geotransform[3]
        xdim = geotransform[1]
        ydim = geotransform[5]*-1
        for i in range(0,nbands):
            band = ds.GetRasterBand(i+1)
            data = band.ReadAsArray(0,0,ncols,nrows)
            self.griddata[:,:,i] = data.copy()
        self.griddata = numpy.squeeze(self.griddata)
        self.geodict['ncols'] = ncols
        self.geodict['nrows'] = nrows
        self.geodict['xdim'] = xdim
        self.geodict['ydim'] = ydim
        self.geodict['xmin'] = ulx
        self.geodict['ymax'] = uly
        self.geodict['xmax'] = self.geodict['xmin'] + ((self.geodict['ncols']-1)*self.geodict['xdim'])
        self.geodict['ymin'] = self.geodict['ymax'] - ((self.geodict['nrows']-1)*self.geodict['ydim'])
        self.geodict['bandnames'] = ['Unknown']

if __name__ == '__main__':
    fname = sys.argv[1]
    tgrid = TiffGrid(fname)
    print tgrid.getRange()
    
