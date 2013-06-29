#!/usr/bin/env python

def hex2rgb(hexcolor):
    """
    Convert hex representation of color ('#FF00AA' or 'FF00AA') into RGB 0-1 tuple.
    Older versions of matplotlib don't accept HTML-style hex representations of color
    """
    if isinstance(hexcolor,str):
        return __hex2rgb__(hexcolor)
    else: #assume that hexcolor is a sequence of some kind
        seqcolor = []
        for color in hexcolor:
            seqcolor.append(__hex2rgb__(color))
            
        return seqcolor

def __hex2rgb__(hexcolor):
    hexlen = len(hexcolor)
    off = 0
    if hexcolor.count('#'):
        off = 1
    return (int(hexcolor[off:off+2],16)/255.,int(hexcolor[off+2:off+4],16)/255.,int(hexcolor[off+4:off+6],16)/255.)

        

                         
