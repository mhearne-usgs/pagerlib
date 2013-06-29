#!/usr/bin/env python

#stdlib imports
import struct
import sys

#third party imports
import numpy
from scipy.io import netcdf
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

#local imports
from grid import Grid

class GMTGrid(Grid):
    def __init__(self,grdfile=None,fmt='f',bandname=None):
        #Valid values for fmt are:
        #'i' (16 bit signed integer)
        #'l' (32 bit signed integer)
        #'f' (32 bit float)
        #'d' (64 bit float)
        self.geodict = {}
        self.griddata = None
        if grdfile is None:
            return

        #check the file size against the supposed format - won't be able to 
        #tell the difference between floats and 32 bit integers though.  should 
        #probably also put that in the function documentation.
        
        f = open(grdfile,'rb')
        f.seek(8,0)
        offset = struct.unpack('I',f.read(4))[0]
        if offset == 0 or offset == 1:
            ftype = 'binary'
        else:
            ftype = 'netcdf'
        
        if ftype == 'netcdf':
            f.close()
            cdf = netcdf.netcdf_file(grdfile)
            self.geodict['nrows'] = cdf.dimensions['y']
            self.geodict['ncols'] = cdf.dimensions['x']
            self.geodict['xmin'] = cdf.variables['x'].data.min()
            self.geodict['xmax'] = cdf.variables['x'].data.max()
            self.geodict['ymin'] = cdf.variables['y'].data.min()
            self.geodict['ymax'] = cdf.variables['y'].data.max()
            #make sure the x and y cell dimensions are reasonably constant
            dx = numpy.diff(cdf.variables['x'].data)
            dy = numpy.diff(cdf.variables['y'].data)
            isXConsistent = numpy.abs(1 - numpy.max(dx)/numpy.min(dx)) < 0.01
            isYConsistent = numpy.abs(1 - numpy.max(dx)/numpy.min(dx)) < 0.01
            if isXConsistent and isYConsistent:
                self.geodict['xdim'] = numpy.mean(dx)
                self.geodict['ydim'] = numpy.mean(dy)
            else:
                raise Exception,'X or Y cell dimensions are not consistent!'
            self.griddata = cdf.variables['z'].data
            self.griddata = numpy.flipud(numpy.copy(self.griddata))
            self.geodict['bandnames'] = ['Unknown']
            cdf.close()
            return

        f.seek(0,0)
        self.geodict = {}
        self.geodict['ncols'] = struct.unpack('I',f.read(4))[0]
        self.geodict['nrows'] = struct.unpack('I',f.read(4))[0]
        offset = struct.unpack('I',f.read(4))[0]
        self.geodict['xmin'] = struct.unpack('d',f.read(8))[0]
        self.geodict['xmax'] = struct.unpack('d',f.read(8))[0]
        self.geodict['ymin'] = struct.unpack('d',f.read(8))[0]
        self.geodict['ymax'] = struct.unpack('d',f.read(8))[0]
        zmin = struct.unpack('d',f.read(8))[0]
        zmax = struct.unpack('d',f.read(8))[0]
        self.geodict['xdim'] = struct.unpack('d',f.read(8))[0]
        self.geodict['ydim'] = struct.unpack('d',f.read(8))[0]
        zscale = struct.unpack('d',f.read(8))[0]
        zoffset = struct.unpack('d',f.read(8))[0]
        xunits = f.read(80).strip()
        yunits = f.read(80).strip()
        zunits = f.read(80).strip()
        title = f.read(80).strip()
        command = f.read(320).strip()
        remark = f.read(160).strip()
        #nota bene - the extent specified in a GMT grid is for the edges of the
        #grid, regardless of whether you've specified grid or pixel
        #registration.
        self.geodict['xmin'] = self.geodict['xmin'] + self.geodict['xdim']/2.0
        self.geodict['xmax'] = self.geodict['xmax'] - self.geodict['xdim']/2.0
        self.geodict['ymin'] = self.geodict['ymin'] + self.geodict['ydim']/2.0
        self.geodict['ymax'] = self.geodict['ymax'] - self.geodict['ydim']/2.0
        if bandname is not None:
            self.geodict['bandnames'] = [bandname]
        else:
            self.geodict['bandnames'] = ['']
        
        sfmt = '%i%s' % (self.geodict['ncols']*self.geodict['nrows'],fmt)
        dwidths = {'i':2,'l':4,'f':4,'d':8}
        dwidth = dwidths[fmt]
        dbytes = f.read(self.geodict['ncols']*self.geodict['nrows']*dwidth)
        data = struct.unpack(sfmt,dbytes)
        self.griddata = numpy.array(data).reshape(self.geodict['nrows'],-1)
        self.griddata = (self.griddata * zscale) + zoffset
        f.close()     

    def save(self,filename,fmt='binary'):
        nrows,ncols = self.griddata.shape
        xmin = self.geodict['xmin'] - self.geodict['xdim']/2.0
        ymax = self.geodict['ymax'] + self.geodict['ydim']/2.0
        xmax = self.geodict['xmax'] + self.geodict['xdim']/2.0
        ymin = self.geodict['ymin'] - self.geodict['ydim']/2.0
        
        
        if fmt != 'binary':
            cdf = netcdf.netcdf_file(filename,'w')
            cdf.createDimension('x',self.geodict['ncols'])
            cdf.createDimension('y',self.geodict['nrows'])
            x = cdf.createVariable('x',numpy.dtype('double'),['x'])
            y = cdf.createVariable('y',numpy.dtype('double'),['y'])
            z = cdf.createVariable('z',self.griddata.dtype,['y','x'])
            xdim = self.geodict['xdim']
            ydim = self.geodict['ydim']
            x[:] = numpy.arange(xmin,xmax+xdim,xdim)
            y[:] = numpy.arange(ymin,ymax+ydim,ydim)
            z.data = self.griddata
            cdf.flush()
            cdf.close()
            return
        if not len(self.geodict):
            raise Exception,'This grid contains no data!'
        zmin = numpy.nanmin(self.griddata)
        zmax = numpy.nanmax(self.griddata)
        f = open(filename,'wb')
        f.write(struct.pack('I',self.geodict['ncols']))
        f.write(struct.pack('I',self.geodict['nrows']))
        f.write(struct.pack('I',1)) #node offset
        f.write(struct.pack('d',xmin))
        f.write(struct.pack('d',xmax))
        f.write(struct.pack('d',ymin))
        f.write(struct.pack('d',ymax))
        f.write(struct.pack('d',zmin))
        f.write(struct.pack('d',zmax))
        f.write(struct.pack('d',self.geodict['xdim']))
        f.write(struct.pack('d',self.geodict['ydim']))
        f.write(struct.pack('d',1)) #z scale factor
        f.write(struct.pack('d',0)) #z offset
        hunits = 'Decimal degrees'
        vunits = 'Unknown'
        title = 'None'
        cmd = 'Generated by a custom Python class'
        remark = 'None'
        hpad = [0 for i in range(0,80-len(hunits))]
        vpad = [0 for i in range(0,80-len(vunits))]
        tpad = [0 for i in range(0,80-len(title))]
        cpad = [0 for i in range(0,320-len(cmd))]
        rpad = [0 for i in range(0,160-len(remark))]
        hfmt = '%ib' % (80-len(hunits))
        vfmt = '%ib' % (80-len(vunits))
        tfmt = '%ib' % (80-len(title))
        cfmt = '%ib' % (320-len(cmd))
        rfmt = '%ib' % (160-len(remark))
        f.write(hunits) #xunits
        f.write(struct.pack(hfmt,*hpad))
        f.write(hunits) #yunits
        f.write(struct.pack(hfmt,*hpad))
        f.write(vunits)
        f.write(struct.pack(vfmt,*vpad))
        f.write(title)
        f.write(struct.pack(tfmt,*tpad))
        f.write(cmd)
        f.write(struct.pack(cfmt,*cpad))
        f.write(remark)
        f.write(struct.pack(rfmt,*rpad))
        dwidths = {'i':2,'l':4,'f':4,'d':8}
        dwidth = dwidths[self.griddata.dtype.kind]
        nrows,ncols = self.griddata.shape
        sfmt = '%i%s' % (nrows*ncols,self.griddata.dtype.kind)
        f.write(struct.pack(sfmt,*self.griddata.transpose().flatten()))
        f.close()
        return
        
if __name__ == '__main__':
    gridfile = sys.argv[1]
    mygrid = GMTGrid(gridfile)
    print 'Here'
    plt.imshow(mygrid.griddata)
    print 'there'
    plt.title('Original image')
    plt.savefig('original.png')
    print 'anywhere'
    plt.close(plt.gcf())
    print 'Here again'
    
    newgridfile = 'output.grd'
    mygrid.save(newgridfile)
    print 'lalala'
    mygrid2 = GMTGrid(newgridfile)
    plt.imshow(mygrid.griddata)
    plt.title('Saved image')
    plt.savefig('saved.png')
    print 'not here'
    #plt.close(plt.gcf())    
    
        
