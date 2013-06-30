#!/usr/bin/env python

#third party
from numpy import testing
import numpy as np

#local libraries
from pagerutil import colors,interp,matutil,text

def test_colors():
    hexinput = '#FF00AA'
    rgboutput = (1,0,0.666666666)
    output = colors.hex2rgb(hexinput)
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
    outmat = np.array([1,2,3,4,1,2,3,4]).reshape(4,2,order='F')
    inmat = np.ones((4,1))
    inmat[0] = 1.
    inmat[1] = 2.
    inmat[2] = 3.
    inmat[3] = 4.
    outmat2 = matutil.repmat(inmat,1,2)
    testing.assert_almost_equal(outmat,outmat2)

def test_sub2ind():
    idx = 5
    mat = np.random.rand(3,3)
    outidx = matutil.sub2ind(mat.shape,(2,1))
    assert outidx == idx

def test_ind2sub():
    sub = (2,1)
    mat = np.random.rand(3,3)
    outsub = matutil.ind2sub(mat.shape,5)
    assert outsub == sub

def test_decToRoman():
    assert text.decToRoman(1025) == 'MXXV'

def test_setNumPrecision():
    assert text.setNumPrecision(531,1) == 500

if __name__ == '__main__':
    test_colors()
    test_interp()
    test_repmat()
    test_sub2ind()
    test_ind2sub()
    test_decToRoman()
    test_setNumPrecision()    



    
