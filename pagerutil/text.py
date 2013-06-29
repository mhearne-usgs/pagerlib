#!/usr/bin/python

#stdlib imports
import re
import sys
import random
from math import floor,ceil,log10

# these two lists serves as building blocks to construct any roman numeral
# just like coin denominations.
# 1000->"M", 900->"CM", 500->"D"...keep on going 
decimalDens=[1000,900,500,400,100,90,50,40,10,9,5,4,1]
romanDens=["M","CM","D","CD","C","XC","L","XL","X","IX","V","IV","I"]
def decToRoman(dec):
    """
    Return roman numeral version of Arabic integer numeral (limit 4000).
    Example::
      decToRoman(11) => 'XI'
      decToRoman(1025) => 'MXXV'
    @param dec: Integer Arabic numeral.
    @return: Roman numeral equivalent of input, as string.
    @raise ValueError: When input is negative or greater or equal to 4000.
    """		
    if dec <=0:
        raise ValueError, "It must be a positive"
        # to avoid MMMM
    elif dec>=4000:  
        raise ValueError, "It must be lower than MMMM(4000)"
    
    return _decToRoman(dec,"",decimalDens,romanDens)

def _decToRoman(num,s,decs,romans):
    """
    convert a Decimal number to Roman numeral recursively
    @param num: the decimal number
    @param s: the roman numerial string
    @param decs: current list of decimal denomination
    @param romans: current list of roman denomination
    @return: Roman numeral equivalent of num, as string.
    """
    if decs:
        if (num < decs[0]):
            # deal with the rest denomination
            return _decToRoman(num,s,decs[1:],romans[1:])		  
        else:
            # deduce this denomation till num<desc[0]
            return _decToRoman(num-decs[0],s+romans[0],decs,romans)	  
    else:
        # we run out of denomination, we are done 
        return s

def setNumPrecision(number,precision,mode='int'):
    """
    Return the input number with N digits of precision
    @param number:  Input value
    @param precision: Number of digits of desired precision
    @return:  Input value with 'precision' digits of precision.
    """
    ndigits = len(str(int(floor(number))))
    value = round(10.0**(precision-1) * number/(10.0**(ndigits-1))) / 10.0**(precision-1)
    value = value * 10.0**(ndigits-1)
    if mode == 'int':
        return int(value)
    else:
        return value

def popRound(value):
    """
    Round population value to nearest 1000, return as human readable string with commas.
    
    Example::
      print popRound(9184) => '10,000'

    @param value: Population value to be rounded.
    @return: "Commified" string form of value, rounded to nearest 1000.
    """
    return commify(roundToNearest(value))

def dollarRound(value,digits=2,mode='short'):
    """
    Return an abbreviated dollar value.
    @param value: Input integer dollar value (i.e., 1000000)
    @keyword mode: 'short' or 'long' (default 'short')
    @keyword digits: Number of significant digits (default 2).
    @return: Rounded string version of dollar amount (i.e., $1.0B or $1.0 Billion
    """
    if value < 1e3:
        return '$'+commify(setNumPrecision(value,digits))
    suffixdict = {'K':1e3,'M':1e6,'B':1e9}
    if mode == 'short':
        if value >= suffixdict['K'] and value < suffixdict['M']:
            return '$%sK' % setNumPrecision(value/1e3,digits,mode='float')
        if value >= suffixdict['M'] and value < suffixdict['B']:
            return '$%sM' % setNumPrecision(value/1e6,digits,mode='float')
        else:
            return '$%sB' % setNumPrecision(value/1e9,digits,mode='float')
    else:
        if value >= suffixdict['K'] and value < suffixdict['M']:
            return '$%s thousand' % setNumPrecision(value/1e3,digits,mode='float')
        if value > suffixdict['M'] and value < suffixdict['B']:
            return '$%s million' % setNumPrecision(value/1e6,digits,mode='float')
        else:
            return '$%s billion' % setNumPrecision(value/1e9,digits,mode='float')

def popRoundShort(value,usemillion=False):
    """
    Return an abbreviated population value (i.e., '1,024k' for 1,024,125, '99k' for 99,125, '9k' for 9,125)
    @param value: Population value to be shortened.
    @keyword usemillion: If True, values greater than 1 million will be appended with 'm'.  Default always appends 'k'.
    @return: String population value with 'k' or 'm' appended (or nothing if 0)
    """
    if value < 1000:
        return str(int(value))
    suffixdict = {'k':1000,'m':1000000}
    if value >= suffixdict['m'] and usemillion:
        suffix = 'm'
    else:
        suffix = 'k'

    roundValue = suffixdict[suffix]
    roundnum = roundToNearest(value)/roundValue
    if roundnum == 0:
        return str(roundnum)
    else:
        return commify(roundnum)+suffix

def roundToNearest(value,roundValue=1000):
    """
    Return the value, rounded to nearest roundValue (defaults to 1000).
    @param value: Value to be rounded.
    @keyword roundValue: Number to which the value should be rounded.
    """
    if roundValue < 1:
        ds = str(roundValue)
        nd = len(ds) - (ds.find('.')+1)
        value = value * 10**nd
        roundValue = roundValue * 10**nd
        value = int(round(float(value)/roundValue)*roundValue)
        value = float(value) / 10**nd
    else:
        value = int(round(float(value)/roundValue)*roundValue)
    
    return value

def floorToNearest(value,floorValue=1000):
    """
    Return the value, floored to nearest floorValue (defaults to 1000).
    @param value: Value to be floored.
    @keyword floorValue: Number to which the value should be floored.
    """
    if floorValue < 1:
        ds = str(floorValue)
        nd = len(ds) - (ds.find('.')+1)
        value = value * 10**nd
        floorValue = floorValue * 10**nd
        value = int(floor(float(value)/floorValue)*floorValue)
        value = float(value) / 10**nd
    else:
        value = int(floor(float(value)/floorValue)*floorValue)
    return value

def ceilToNearest(value,ceilValue=1000):
    """
    Return the value, ceiled to nearest ceilValue (defaults to 1000).
    @param value: Value to be ceiled.
    @keyword ceilValue: Number to which the value should be ceiled.
    """
    if ceilValue < 1:
        ds = str(ceilValue)
        nd = len(ds) - (ds.find('.')+1)
        value = value * 10**nd
        ceilValue = ceilValue * 10**nd
        value = int(ceil(float(value)/ceilValue)*ceilValue)
        value = float(value) / 10**nd
    else:
        value = int(ceil(float(value)/ceilValue)*ceilValue)
    return value


    
def commify(num, separator=','):
    """Return a string representing the number num with separator inserted for every power of 1000.
    
    commify(1234567) -> '1,234,567'
    
    @param num: Number to be formatted.
    @keyword separator: Separator to be used.
    @return: "Commified" string.
    """
    regex = re.compile(r'^(-?\d+)(\d{3})')
    num = str(num)  # just in case we were passed a numeric value
    more_to_do = 1
    while more_to_do:
        (num, more_to_do) = regex.subn(r'\1%s\2' % separator,num)
    return num

def justifyLine(line, width):
    """Stretch a line to width by filling in spaces at word gaps.

    The gaps are picked randomly one-after-another, before it starts
    over again.

    """
    i = []
    while 1:
        # line not long enough already?
        if len(' '.join(line)) < width:
            if not i:
                # index list is exhausted
                # get list if indices excluding last word
                i = range(max(1, len(line)-1))
                # and shuffle it
                random.shuffle(i)
            # append space to a random word and remove its index
            line[i.pop(0)] += ' '
        else:
            # line has reached specified width or wider
            return ' '.join(line)

def fillParagraphs(text, width=80, justify=0):
    """Split a text into paragraphs and wrap them to width linelength.

    Optionally justify the paragraphs (i.e. stretch lines to fill width).

    Inter-word space is reduced to one space character and paragraphs are
    always separated by two newlines. Indention is currently also lost.

    """
    # split text into paragraphs at occurences of two or more newlines
    paragraphs = re.split(r'\n\n+', text)
    for i in range(len(paragraphs)):
        # split paragraphs into a list of words
        words = paragraphs[i].strip().split()
        line = []; new_par = []
        while 1:
           if words:
               if len(' '.join(line + [words[0]])) > width and line:
                   # the line is already long enough -> add it to paragraph
                   if justify:
                       # stretch line to fill width
                       new_par.append(justifyLine(line, width))
                   else:
                       new_par.append(' '.join(line))
                   line = []
               else:
                   # append next word
                   line.append(words.pop(0))
           else:
               # last line in paragraph
               new_par.append(' '.join(line))
               line = []
               break
        # replace paragraph with formatted version
        paragraphs[i] = '\n'.join(new_par)
    # return paragraphs separated by two newlines
    return '\n\n'.join(paragraphs)
