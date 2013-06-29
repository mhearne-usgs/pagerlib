#!/usr/bin/env python

#stdlib imports
import datetime

def timeForXML(dtime):
    """
    Convert datetime object (in UTC) to XML dateTime format, i.e. 2002-05-30T09:30:10Z
    @param dtime: Datetime object, presumed already referenced to UTC.
    @return: String representing that datetime object in the XML dateTime datatype format.
    """
    fmt = '%Y-%m-%dT%H:%M:%SZ'
    return dtime.strftime(fmt)

def getTimeElapsed(time1,time2):
    td = time2 - time1
    nseconds = 0
    nminutes = 0
    nhours = 0
    ndays = 0
    nweeks = 0
    nseconds = td.seconds + td.days*86400
    if nseconds >= 60:
        nminutes = nseconds/60
        nseconds = round(((nseconds/60.0)-nminutes)*60)
        if nminutes >= 60:
            nhours = nminutes/60
            nminutes = round(((nminutes/60.0)-nhours)*60)
            if nhours >= 24:
                ndays = nhours/24
                nhours = round(((nhours/24.0)-ndays)*24)
                if ndays >= 7:
                    nweeks = ndays/7
                    ndays = round(((ndays/7.0)-nweeks)*7)
    return (nweeks,ndays,nhours,nminutes,nseconds)

def getTimeElapsedString(thentime,nowtime):
    """
    Return string describing time elapsed between first input time and now, or first and second input times.
    @param thentime: Input datetime object (in the past).
    @keyword nowtime: Input datetime object (forward in time from thentime).
    @return: String describing elapsed time in the two longest applicable units of time, up to years.
             '10 minutes, 30 seconds', '10 hours, 47 minutes', '10 days, 23 hours', '10 months, 22 days', etc.
    """
    nweeks,ndays,nhours,nminutes,nseconds = getTimeElapsed(thentime,nowtime)
    if nweeks:
        return getTimeStr(nweeks,ndays,'week')
    if ndays:
        return getTimeStr(ndays,nhours,'day')
    if nhours:
        return getTimeStr(nhours,nminutes,'hour')
    if nminutes:
        return getTimeStr(nminutes,nseconds,'minute')
    if nseconds != 1:
        return '%i seconds' % (nseconds)
    else:
        return '1 second'

def getTimeStr(bigtime,smalltime,unit):
    """
    Return a time string describing elapsed time.
    @param bigtime:  Number of years, months, days, hours, or minutes.
    @param smalltime: Number of months, days, hours, minutes, or seconds.
    @param unit: String representing the units of bigtime, one of: 'second','minute','hour','day','week','month','year'.
    @return: String elapsed time ('10 days, 13 hours').
    """
    periods = ['second','minute','hour','day','week','month','year']
    bigunit = periods[periods.index(unit)]
    smallunit = periods[periods.index(unit)-1]
    if bigtime != 1:
        bigunit = bigunit+'s'
    if smalltime != 1:
        smallunit = smallunit+'s'
    return '%s %s, %i %s' % (bigtime,bigunit,smalltime,smallunit)

if __name__ == '__main__':
    tnow = datetime.datetime.now()
    
    offset = 10 #10 seconds before
    print getTimeElapsedString(tnow - datetime.timedelta(seconds=offset))

    offset = 75 #1 minute, 15 seconds before
    print getTimeElapsedString(tnow - datetime.timedelta(seconds=offset))

    offset = int(1.77*3600) #1.77 hours before
    print getTimeElapsedString(tnow - datetime.timedelta(seconds=offset))
    
    offset = int(1.5*3600*24) #1.5 days before
    print getTimeElapsedString(tnow - datetime.timedelta(seconds=offset))
    
    offset = int(9.5*3600*24) #9.5 days before
    print getTimeElapsedString(tnow - datetime.timedelta(seconds=offset))

    offset = int(36.5*3600*24) #36.5 days before
    print getTimeElapsedString(tnow - datetime.timedelta(seconds=offset))

    offset = int(382*3600*24) #382 days before
    print getTimeElapsedString(tnow - datetime.timedelta(seconds=offset))

    offset = 150*365 #150 years before
    print getTimeElapsedString(tnow - datetime.timedelta(days=offset))

