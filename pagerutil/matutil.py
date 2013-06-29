#!/usr/bin/python
from numpy import array,prod
def repmat(a, m, n):
    """
    Mimic the behavior of Matlab's repmat() function.
    @param a: 2D numpy array.
    @param m: Desired number of output rows.
    @param n: Desired number of output columns.
    @return: 2D numpy array consisting of input array replicated M rows by N columns.
    """
    if a.ndim == 1:
        a = array([a])
    (origrows, origcols) = a.shape
    rows = origrows * m
    cols = origcols * n
    b = a.reshape(1,a.size).repeat(m, 0).reshape(rows, origcols).repeat(n, 0)
    return b.reshape(rows, cols)

def sub2ind(shape,subtpl):
    """
    Convert 2D subscripts into 1D index.
    @param shape: Tuple indicating size of 2D array.
    @param subtpl: Tuple of (possibly) numpy arrays of row,col values.
    @return: 1D array of indices.
    """
    if len(shape) != 2 or len(shape) != len(subtpl):
        raise IndexError, "Input size and subscripts must have length 2 and be equal in length"
    
    row,col = subtpl
    nrows,ncols = shape
    ind = col*nrows + row
    return ind
    
def ind2sub(shape,ind):
    """
    Convert 1D indices into 2D subscripts.
    @param shape: Tuple indicating size of 2D array.
    @param ind: 1D array of indices.
    @return: Tuple of (possibly) numpy arrays of row,col values.
    """
    if len(shape) != 2:
        raise IndexError, "Input size must have length 2 and index must be inside array."

    m,n = shape
    
    i = ind % m
    j = ind // m

    return (i,j)
