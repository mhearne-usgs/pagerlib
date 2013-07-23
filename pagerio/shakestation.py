#!/usr/bin/env python

#standard library
import re
from xml.dom import minidom
from datetime import datetime
import sys

#third party
import pandas as pd
import numpy as np

TIMEFMT = '%m/%d/%Y %H:%M:%S'

def parseLine1(line):
    eqdict = {}
    parts = line.split(',')
    time = datetime.strptime(parts[0][parts[0].find(':')+1:-3].strip(),TIMEFMT)
    eqdict['time'] = time
    eqdict['mag'] = float(re.findall('[0-9]*\.[0-9]',parts[1])[0])
    eqdict['lat'] = float(parts[2].split(':')[1].strip())
    eqdict['lon'] = float(parts[3].split(':')[1].strip())
    depstr = parts[4].split(':')[1].strip().replace('km','')
    eqdict['depth'] = float(depstr)
    biasparts = parts[5].split(':')[1].strip().split()
    for bpart in biasparts:
        key,value = bpart.split('=')
        eqdict['bias_'+key] = float(value)
    return eqdict

def parseLine2(line):
    parts = line.split(':')
    tmpcolumns = parts[1].strip().split(',')
    columns = []
    for column in tmpcolumns:
        column = column.strip()
        match = re.search('\(([^\)]+)\)',column) #match everything inside ()
        if match is not None:
            column = column.replace(match.group(),'').strip()
        columns.append(column)
    return columns

def readStation(stationfile):
    f = open(stationfile,'rt')
    line = f.readline()
    eqdict = parseLine1(line)
    line = f.readline()
    columns = parseLine2(line)
    line = f.readline()
    ncolumns = 0
    rows = []
    for line in f.readlines():
        parts = line.split(',')
        rowparts = []
        for p in parts:
            try:
                p = float(p)
            except:
                p = p.replace('\\n','').strip()
            rowparts.append(p)
        if len(parts) > ncolumns:
            ncolumns = len(parts)
        rows.append(rowparts)
    f.close()
    df = pd.DataFrame(np.ones((len(rows),ncolumns))*np.NaN)
    irow = 0
    for row in rows:
        ncols = len(row)
        df.iloc[irow,0:ncols] = row
        irow += 1
    

if __name__ == '__main__':
    readStation(sys.argv[1])
    
