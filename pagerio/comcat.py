#!/usr/bin/env python

#stdlib imports
import urllib2
import urllib
import json
import os.path
from datetime import datetime
import re

URLBASE = 'http://comcat.cr.usgs.gov/fdsnws/event/1/query?%s'
TIMEFMT = '%Y-%m-%dT%H:%M:%S'

def getContents(product,contentlist,outfolder=None,bounds = None,
                starttime = None,endtime = None,magrange = None,
                catalog = None,contributor = None,eventid = None):
    
    if catalog is not None and catalog not in checkCatalogs():
        raise Exception,'Unknown catalog %s' % catalog
    if contributor is not None and contributor not in checkContributors():
        raise Exception,'Unknown contributor %s' % contributor

    #start creating the url parameters
    urlparams = {}
    urlparams['producttype'] = product
    if starttime is not None:
        urlparams['starttime'] = starttime.strftime(TIMEFMT)
        if endtime is None:
            urlparams['endtime'] = datetime.utcnow().strftime(TIMEFMT)
    if endtime is not None:
        urlparams['endtime'] = endtime.strftime(TIMEFMT)
        if starttime is None:
            urlparams['starttime'] = datetime(1900,1,1,0,0,0).strftime(TIMEFMT)

    #we're using a rectangle search here
    if bounds is not None:
        urlparams['minlongitude'] = bounds[0]
        urlparams['maxlongitude'] = bounds[1]
        urlparams['minlatitude'] = bounds[2]
        urlparams['maxlatitude'] = bounds[3]

    if magrange is not None:
        urlparams['minmagnitude'] = magrange[0]
        urlparams['maxmagnitude'] = magrange[1]
    
    if catalog is not None:
        urlparams['catalog'] = catalog
    if contributor is not None:
        urlparams['contributor'] = contributor

    #search parameters we're not making available to the user (yet)
    urlparams['orderby'] = 'time-asc'
    urlparams['format'] = 'geojson'

    if outfolder is None:
        outfolder = os.getcwd()
    params = urllib.urlencode(urlparams)
    url = URLBASE % params
    fh = urllib2.urlopen(url)
    feed_data = fh.read()
    fh.close()
    fdict = json.loads(feed_data)

    outfiles = []
    for feature in fdict['features']:
        eid = feature['id']
        lat,lon,depth = feature['geometry']['coordinates']
        mag = feature['properties']['mag']
        furl = feature['properties']['url']+'.json'
        fh = urllib2.urlopen(furl)
        event_data = fh.read()
        fh.close()
        edict = json.loads(event_data)
        pdict = edict['products'][product][0]
        if pdict['status'].lower() == 'delete':
            continue
        for content in contentlist:
            for contentkey in pdict['contents'].keys():
                if re.search(content,contentkey) is not None:
                    contenturl = pdict['contents'][contentkey]['url']
                    fh = urllib2.urlopen(contenturl)
                    data = fh.read()
                    fh.close()
                    outfile = os.path.join(outfolder,'%s_%s' % (eid,content))
                    f = open(outfile,'w')
                    f.write(data)
                    f.close()
                    outfiles.append(outfile)

    return outfiles
                
if __name__ == '__main__':
    #california bbox
    xmin = -125.15625
    xmax = -113.774414
    ymin = 32.600048
    ymax = 41.851151
    mintime = datetime(1900,1,1)
    maxtime = datetime.utcnow()
    bounds = (xmin,xmax,ymin,ymax)
    outlist = getContents('shakemap',['stationlist.txt'],
                          outfolder='/Users/mhearne/tmp/',
                          bounds=bounds,starttime=mintime,endtime=maxtime)
