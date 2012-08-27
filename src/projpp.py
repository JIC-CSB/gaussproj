#!/usr/bin/env python2.7

import os, sys, scipy
import scipy.misc
import scipy.ndimage as nd
import Image
import numpy as np

def numpy_draw_pil(r):
    i = Image.fromarray(r)
    i.show()

def print_transfer_fn(fn):
    for i in range(0, 255, 10):
        print "%d: %d" % (i, fn[i])

def gen_transfer_fn():
    d = {}
    t = 75
    for i in range(0, 256):
        if i < t:
            d[i] = 0
        else:
            d[i] = 255

    return d

def np_iter(na):
    xmax, ymax = na.shape

    return ((x, y) for x in range(0, xmax) for y in range(0, ymax))

def np_e(na):
    xmax, ymax = na.shape
    return np.empty([xmax, ymax], dtype = np.uint8)

def apply_transfer_fn(na, fn):
    ni = np_iter(na)

    nout = np_e(na)

    # TODO - nice fp way of doing this with real functions
    for x, y in ni:
        nout[x, y] = fn[na[x, y]]

    return nout
    

def main():
    #filename = 'output/surface-g3d-30-30-7.png'
    filename = 'output/proj-g3d-30-30-7.png'
    raw = scipy.misc.imread(filename)

    fn = gen_transfer_fn()
    print_transfer_fn(fn)
    
    thresh = apply_transfer_fn(raw, fn)

    numpy_draw_pil(thresh)

    alpha = 1
    fl = nd.gaussian_filter(raw, 1.0)
    sharpened = thresh + alpha * (thresh - fl)
    numpy_draw_pil(sharpened)

if __name__ == "__main__":
    main()
