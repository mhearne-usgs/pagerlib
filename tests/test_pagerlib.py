#!/usr/bin/env python

#third party
from numpy import testing
import numpy as np

#local libraries
from pagerlib import pagerio
from pagerlib import pagerutil

def test_colors():
    hexinput = '#FF00AA'
    rgboutput = (1,0,0.39215686274509803)
    output = pagerutil.colors.hex2rgb(hexinput)
    for pair in zip(rgboutput,output):
        testing.assert_almost_equal(pair[0],pair[1])

def test_interp():
    zout = np.array([2.5,3.5,6.5,7.5]).reshape(2,2)
    z = np.arange(0,16).reshape(4,4)
    xi = np.arange(0.5,2.5,1)
    yi = np.arange(0.5,2.5,1)
    zi = interp.interp2(z,xi,yi)
    testing.assert_almost_equal(zout,zi)

def test_repmat():
    outmat = np.array([1,2,3,4,1,2,3,4])
    inmat = np.array([1,2,3,4])
    outmat2 = pagerutil.matutil.repmat(inmat,1,2)
    testing.assert_almost_equal(outmat,outmat2)

def test_sub2ind():
    idx = 5
    mat = np.array([1,2,3,4,5,6,7,8,9]).reshape(3,3)
    outidx = pagerutil.matutil.sub2ind(mat.shape,(2,2))
    assert outidx == idx

def test_ind2sub():
    sub = (2,2)
    mat = np.array([1,2,3,4,5,6,7,8,9]).reshape(3,3)
    outsub = pagerutil.matutil.ind2sub(mat.shape,5)
    assert outidx == idx

def test_decToRoman(dec):
    assert pagerutil.text.decToRoman(1025) == 'MXXV'

def test_setNumPrecision():
    assert pagerutil.text.setNumPrecision(531,1) == 500




    
