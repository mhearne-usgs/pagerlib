#!/usr/bin/env python

#stdlib
import os.path
import struct
from collections import OrderedDict

#third party imports
from mpl_toolkits.basemap import shapefile
from numpy import array,concatenate,nan

def rectint(r1,r2):
    #rects are xmin,xmax,ymin,ymax
    separate =  r1[1] < r2[0] or r1[0] > r2[1] or r1[3] < r2[2] or r1[2] > r2[3]
    return not separate

class PagerShapeFile(object):
    """
    Read information from an ESRI Shapefile.
    """
    # reader = None
    # bounds = None
    # shpfilename = None
    shpdict = {1:'point',3:'line',5:'polygon',8:'multipoint'}
    dbfdict = {'C':'string','N':'number','F':'float','D':'double'}
    # shapeType = None
    # nShapes = 0
    # attributes = OrderedDict()
    # hasIndex = False
    def __init__(self,shapefilename):
        """
        Construct a PagerShapeFile object.
        @param shapefile: Name of shape file (.shp).  Must be accompanied by .shx, .dbf files.
        """
        try:
            self.reader = shapefile.Reader(shapefilename)
        except:
            raise IOError, 'error reading shapefile %s.shp' % shapefile
        self.shapefilename = shapefilename
        self.shapeType = self.shpdict[self.reader.shape(0).shapeType]
        self.bounds = (self.reader.bbox[0],self.reader.bbox[2],self.reader.bbox[1],self.reader.bbox[3])
        self.nShapes = self.reader.numRecords
        f,e = os.path.splitext(shapefilename)
        indexfile = f + '.spx'
        if os.path.isfile(indexfile):
            self.hasIndex = True
        self.getAttributes()

    def getShapesByBoundingBox(self,bbox):
        #bbox is a tuple consisting of (xmin,xmax,ymin,ymax)
        #i = int, d = double
        if self.hasIndex:
            f,e = os.path.splitext(self.shapefilename)
            indexfile = f + '.spx'
            f = open(indexfile,'rb')
            #read header
            nrows = struct.unpack('i',f.read(4))[0]
            ncols = struct.unpack('i',f.read(4))[0]
            xmin = struct.unpack('d',f.read(8))[0]
            xmax = struct.unpack('d',f.read(8))[0]
            ymin = struct.unpack('d',f.read(8))[0]
            ymax = struct.unpack('d',f.read(8))[0]
            xdim = struct.unpack('d',f.read(8))[0]
            ydim = struct.unpack('d',f.read(8))[0]
            allshapes = set()
            for i in range(0,nrows):
                for j in range(0,ncols):
                    txmin = struct.unpack('d',f.read(8))[0]
                    txmax = struct.unpack('d',f.read(8))[0]
                    tymin = struct.unpack('d',f.read(8))[0]
                    tymax = struct.unpack('d',f.read(8))[0]
                    nshapes = struct.unpack('i',f.read(4))[0]
                    fmt = str(nshapes)+'i'
                    ishapes = struct.unpack(fmt,f.read(nshapes*4))
                    if rectint(bbox,(txmin,txmax,tymin,tymax)):
                        allshapes = allshapes.union(set(ishapes))
            f.close()
            allshapes = [shp-1 for shp in list(allshapes)]
            if not len(allshapes):
                return []
            shapes = self.getShapes(indices=allshapes)
            return shapes
        else:
            return []
            
    def getAttributes(self):
        """
        Return a dictionary of column names/types from the DBF file.
        @return:  Dictionary of field names, with possible field type values of: 'string','integer','double','invalid'.
        """
        if hasattr(self,'attributes'):
            return self.attributes
        self.attributes = OrderedDict()

        nfields = len(self.reader.fields)
        for i in range(1,nfields):
            info = self.reader.fields[i]
            self.attributes[info[0]] = self.dbfdict[info[1]]

        return self.attributes

    def __del__(self):
        del self.reader

    def getShape(self,index):
        """
        Return a shape dictionary.
        @param index:  Shape index from 0 to PagerShapeFile.nShapes-1.
        @return: Shape dictionary containing the following keys:
                 'geometry'    - 'point','multipoint','line','polygon'.
                 'boundingbox' - (xmin,xmax,ymin,ymax)
                 'x'           - X vector of data, segments separated by numpy.nan
                 'y'           - Y vector of data, segments separated by numpy.nan
                 'nparts'      - Nuumber of segments (always 1 for point and multipoint)
                 'attr1'       - First attribute in accompanying .dbf file.
                 ...
                 'attrN'       - Nth attribute in accompanying .dbf file.
        """
        shape = self.reader.shape(index)
        shapedict = {}
        shapedict['geometry'] = self.shpdict[self.reader.shape(index).shapeType]
        bbox = self.reader.shape(index).bbox
        shapedict['boundingbox'] = (bbox[0],bbox[2],bbox[1],bbox[3])
        points = shape.points
        parts = shape.parts
        parts.append(len(points))
        istart = parts[0]
        xpoints = []
        ypoints = []
        for j in range(0,len(parts)-1):
            if len(parts) == 1:
                iend = len(points)
            else:
                iend = parts[j+1]
            sx = [p[0] for p in points[istart:iend]]
            sy = [p[1] for p in points[istart:iend]]
            if len(xpoints):
                xpoints = xpoints + [float('nan')] + sx
                ypoints = ypoints + [float('nan')] + sy
            else:
                xpoints = xpoints + sx
                ypoints = ypoints + sy
        shapedict['x'] = array(xpoints)
        shapedict['y'] = array(ypoints)
        shapedict['nparts'] = len(shape.parts)
        try:
            record = self.reader.record(index)
        except:
            pass
        keys = self.attributes.keys()
        for i in range(0,len(keys)): #I can only do this because I'm using an OrderedDict
            key = keys[i]
            shapedict[key] = record[i]
        return shapedict

    def getShapes(self,indices=None):
        """
        Return a list of shape dictionaries.
        @keyword indices:  Sequence of shape indices with values from 0 to PagerShapeFile.nShapes-1.  Default reads all shapes.
        @return: List of shape dictionaries (see getShape())
        """
        if indices is not None:
            if min(indices) < 0 or max(indices) > self.nShapes-1:
                raise LookupError, 'Indices must all be between 0 and %i' % self.nShapes-1
        else:
            indices = range(0,self.nShapes)
        
        shapes = []
        for idx in indices:
            shapes.append(self.getShape(idx))

        return shapes

    def getShapesByAttr(self,field,value):
        """
        Return only those shapes which match a particular value of a given field.
        @param field: Field name to search.
        @param value: Field value against which record fields should be compared.
        @return: List of shape dictionaries (see getShapes()).
        """
        keys = self.attributes.keys()
        values = self.attributes.values()
        if field not in keys:
            raise LookupError, 'Field %s not in shapefile attributes: %s' % (field, str(keys))
        keyidx = keys.index(field)
        shapes = []
        for i in range(0,self.nShapes):
            record = self.reader.record(i)
            if record[keyidx] == value:
                shapes.append(self.getShape(i))
        return shapes
