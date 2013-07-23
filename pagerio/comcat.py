#!/usr/bin/env python

#stdlib imports
import urllib2
import urllib
import json
import os.path
from datetime import datetime,timedelta
import re
from xml.dom import minidom 
import sys
import shutil

URLBASE = 'http://comcat.cr.usgs.gov/fdsnws/event/1/query?%s'
CHECKBASE = 'http://comcat.cr.usgs.gov/fdsnws/event/1/%s'
EVENTURL = 'http://comcat.cr.usgs.gov/earthquakes/eventpage/[EVENTID].json'
TIMEFMT = '%Y-%m-%dT%H:%M:%S'

def checkCatalogs():
    """
    Return the list of valid ComCat catalogs.
    """
    url = CHECKBASE % 'catalogs'
    catalogs = []
    try:
        fh = urllib2.urlopen(url)
        data = fh.read()
        dom = minidom.parseString(data)
        fh.close()
        catalog_elements = dom.getElementsByTagName('Catalog')
        for catel in catalog_elements:
            if catel.firstChild is None:
                continue
            catalog = catel.firstChild.data.strip()
            if len(catalog):
                catalogs.append(str(catalog))
    except:
        raise Exception,"Could not open %s to search for list of catalogs" % url
    return catalogs    

def checkContributors():
    """
    Return the list of valid ComCat contributors.
    """
    url = CHECKBASE % 'contributors'
    contributors = []
    try:
        fh = urllib2.urlopen(url)
        data = fh.read()
        dom = minidom.parseString(data)
        fh.close()
        contributor_elements = dom.getElementsByTagName('Contributor')
        for catel in contributor_elements:
            if catel.firstChild is None:
                continue
            contributor = catel.firstChild.data.strip()
            if len(contributor):
                contributors.append(str(contributor))
    except:
        raise Exception,"Could not open %s to search for list of contributors" % url
    return contributors    

def getContents(product,contentlist,outfolder=None,bounds = None,
                starttime = None,endtime = None,magrange = None,
                catalog = None,contributor = None,eventid = None,
                eventProperties=None,productProperties=None,listURL=False):
    """
    Download product contents for event(s) from ComCat, given a product type and list of content files for that product.

    The possible product types include, but are not limited to:
     - origin
     - focal-mechanism
     - moment-tensor
     - shakemap
     - dyfi
     - losspager

    The possible list of contents is long, suffice it to say that you can figure out the name of the 
    content you want by exploring the "Downloads" tab of an event page.  For example, if you specify 
    "shakemap" in the "Search Downloads" box, you should see a long list of possible downloads.  Mouse \
    over the link for the product(s) of interest and note the file name at the end of the url.  Examples
    for ShakeMap include: "stationlist.txt", "stationlist.xml", "grid.xml".

    @param product: Name of desired product (i.e., shakemap).
    @param contentlist: List of desired contents.
    @keyword outfolder: Local directory where output files should be written (defaults to current working directory).
    @keyword bounds: Sequence of (lonmin,lonmax,latmin,latmax)
    @keyword starttime: Start time for search (defaults to ~30 days ago). YYYY-mm-ddTHH:MM:SS
    @keyword endtime: End time for search (defaults to now). YYYY-mm-ddTHH:MM:SS
    @keyword magrange: Sequence of (minmag,maxmag)
    @keyword catalog: Product catalog to use to constrain the search (centennial,nc, etc.).
    @keyword contributor: Product contributor, or who sent the product to ComCat (us,nc,etc.).
    @keyword eventid: Event id to search for - restricts search to a single event (usb000ifva)
    @keyword eventProperties: Dictionary of event properties to match. {'reviewstatus':'approved'}
    @keyword productProperties: Dictionary of event properties to match. {'alert':'yellow'}
    @return: List of output files.
    @raise Exception: When:
      - Input catalog is invalid.
      - Input contributor is invalid.
      - Eventid was supplied, but not found in ComCat.
    """
    
    if catalog is not None and catalog not in checkCatalogs():
        raise Exception,'Unknown catalog %s' % catalog
    if contributor is not None and contributor not in checkContributors():
        raise Exception,'Unknown contributor %s' % contributor

    if outfolder is None:
        outfolder = os.getcwd()

    #make the output folder if it doesn't already exist
    if not os.path.isdir(outfolder):
        os.makedirs(outfolder)
    
    #if someone asks for a specific eventid, then we can shortcut all of this stuff
    #below, and just parse the event json
    if eventid is not None:
        try:
            outfiles = readEventURL(product,contentlist,outfolder,eventid,listURL=listURL)
            return outfiles
        except:
            raise Exception,'Could not retrieve data for eventid "%s"' % eventid
    
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
    params = urllib.urlencode(urlparams)
    url = URLBASE % params
    fh = urllib2.urlopen(url)
    feed_data = fh.read()
    fh.close()
    fdict = json.loads(feed_data)
    outfiles = []
    for feature in fdict['features']:
        if eventProperties is not None:
            skip=False
            for key,value in eventProperties.iteritems():
                if not feature['properties'].has_key(key):
                    skip=True
                    break
                else:
                    fvalue = feature['properties'][key]
                    if fvalue is None:
                        skip=True
                        break
                    if fvalue.lower() != value.lower():
                        skip=True
                        break
            if skip:
                continue
        eid = feature['id']
        lat,lon,depth = feature['geometry']['coordinates']
        mag = feature['properties']['mag']
        efiles = readEventURL(product,contentlist,outfolder,eid,listURL=listURL,productProperties=productProperties)
        outfiles += efiles

    return outfiles

def readEventURL(product,contentlist,outfolder,eid,listURL=False,productProperties=None):
    """
    Download contents for a given event.

    @param product: Name of desired product (i.e., shakemap).
    @param contentlist: List of desired contents.
    @param outfolder: Local directory where output files should be written (defaults to current working directory).
    @param eid: Event ID to search for.
    @returns: List of downloaded files.
    @raise Exception: When eventid URL could not be parsed.
    """
    outfiles = []
    furl = EVENTURL.replace('[EVENTID]',eid)
    try:
        fh = urllib2.urlopen(furl)
        event_data = fh.read()
        fh.close()
        edict = json.loads(event_data)
        pdict = edict['products'][product][0]

        skip = False
        if productProperties is not None:
            for key,value in productProperties.iteritems():
                if pdict['properties'].has_key(key) and pdict['properties'][key] is not None:
                    if value.lower() != pdict['properties'][key].lower():
                        skip=True
                        break
                
        if skip:
            return outfiles
        if pdict['status'].lower() == 'delete':
            return []
        for content in contentlist:
            for contentkey in pdict['contents'].keys():
                path,contentfile = os.path.split(contentkey)
                if contentfile.lower() == content.lower():
                    contenturl = pdict['contents'][contentkey]['url']
                    if listURL:
                        print contenturl
                        continue
                    fh = urllib2.urlopen(contenturl)
                    print 'Downloading %s...' % contenturl
                    data = fh.read()
                    fh.close()
                    outfile = os.path.join(outfolder,'%s_%s' % (eid,contentfile))
                    f = open(outfile,'w')
                    f.write(data)
                    f.close()
                    outfiles.append(outfile)
    except Exception,msg:
        raise Exception,'Could not parse event information from "%s". Error: "%s"' % (furl,msg.message)
    return outfiles

if __name__ == '__main__':
    #test catalog/contributor checkers
    catalogs = checkCatalogs()
    print 'Catalogs are:'
    print catalogs
    print
    print 'Contributors are:'
    contributors = checkContributors()
    print contributors
    print

    #Downloads all of the shakemap stationlist.txt files for this California bounding box
    #within the last year
    #california bbox
    xmin = -125.15625
    xmax = -113.774414
    ymin = 32.600048
    ymax = 41.851151
    maxtime = datetime.utcnow()
    mintime = maxtime - timedelta(days=60)
    bounds = (xmin,xmax,ymin,ymax)
    outfolder = os.path.join(os.path.expanduser('~'),'tmpcomcatdata')
    outlist = getContents('shakemap',['stationlist.txt'],
                          outfolder = outfolder,
                          bounds=bounds,starttime=mintime,endtime=maxtime)
    print 'Downloaded %i files to %s.  Now deleting those files and the folder.' % (len(outlist),outfolder)
    shutil.rmtree(outfolder)

    #Get the shakemap grid from just a single event - let's choose Northridge
    eventid = 'pde19940117123055390_18'
    outlist = getContents('shakemap',['grid.xml'],
                          outfolder = outfolder,eventid=eventid)
    print 'I downloaded:'
    print outlist
    print 'Now cleaning up...'
    shutil.rmtree(outfolder)
    print 'Done.'
    
