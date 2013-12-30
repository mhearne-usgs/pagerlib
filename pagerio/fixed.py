#!/usr/bin/env python

#stdlib imports
import re
import math

class FixedFormatError(Exception):
    """used for noting errors with FixedFormatWriter and Reader"""

def getFixedFormatString(speclist,vlist):
    """
    Create a fixed format string given the line specification and a list of values.
    @parameter speclist: List of tuples, where each tuple contains:
                         - a sub-tuple containing the start/stop positions of the value in the line (1 offset). 
                         - A FORTRAN format string
    @parameter vlist:    A list of values, which must match the format strings given in speclist,
                         with the following exception: A NaN value where the spec says float or int
                         is OK.  Spaces will be inserted for the NaN value.
    @return: Formatted string (no newline at the end).
    """
    if len(speclist) != len(vlist):
        raise FixedFormatError,'speclist length != vlist length' 
    width = 0
    widths = []
    ftrans = {'a':'s','i':'i','f':'f'}
    numberpattern = r'[-+]?[0-9]*\.?[0-9]+'
    formatstr = ''
    formatlist = []
    offset = 1
    for i in range(0,len(speclist)):
        spec = speclist[i]
        v = vlist[i]
        #if there are spaces between the last offset and the beginning of this one,
        #add them to the format string for the line
        specrange = spec[0]
        smin = specrange[0]
        smax = specrange[1]
        specwidth = (smax-smin)+1
        spaces = ' '*(smin-offset)
        formatstr += spaces
        fmt = spec[1]
        match = re.search(numberpattern,fmt)
        numstr = fmt[match.start():match.end()]
        match = re.search('[a-z]',fmt)
        strstr = fmt[match.start():match.end()]
        if numstr.find('.') > -1:
            width = int(numstr.split('.')[0])
        else:
            width = int(numstr)
        if width != specwidth:
            fmtstring = 'Cannot reconcile format string "%s" with range (%i,%i)'
            raise FixedFormatError,fmtstring % (fmt,smin,smax)
        widths.append(width)
        isfloat = isinstance(v,float)
        if isfloat and math.isnan(v):
            isnumber = fmt.find('i') > -1 or fmt.find('f') > -1
            if isnumber:
                fmt = '%' + str(width) + 's'
                vlist[i] = ' '
            else:
                raise FixedFormatError,'String types do not support NaN values.'
        else:
            fmt = '%' + numstr + ftrans[strstr]
        formatlist.append(fmt)
        formatstr += fmt
        offset = smax+1
    try:
        string = formatstr % tuple(vlist)
        return string
    except:
        raise FixedFormatError,'Could not make a string from "%s" and "%s"' % (formatstr,','.join(vlist))

    
if __name__ == '__main__':
    speclist = [((2,2),'a1'),
                ((3,3),'a1'),
                ((17,19),'a3'),
                ((21,25),'a5'),
                ((30,32),'a3'),
                ((37,39),'a3'),
                ((44,46),'a3'),
                ((51,53),'a3'),
                ((58,60),'a3'),
                ((65,67),'a3'),
                ((69,72),'a4'),
                ((74,77),'a4'),
                ((79,86),'a8'),
                ((87,87),'a1')]
    
    tpl = ['(','#','eM0','eCLVD','eRR','eTT','ePP','eRT','eTP','ePR','NCO1','NCO2','Duration',')']
    print getFixedFormatString(speclist,tpl)

    tpl = ['fred',float('nan'),5]
    speclist = [((1,4),'a4'),
                ((6,10),'f5.3'),
                ((12,14),'i3')]
    print getFixedFormatString(speclist,tpl)
            
    
    

            
