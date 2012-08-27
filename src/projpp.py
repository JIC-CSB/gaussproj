#!/usr/bin/env python2.7

import os, sys, scipy, math
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

def sigmoidal_trans(midp, sf):
    d = {}
    for i in range(0, 256):
        d[i] = 255 - 255 / (1 + math.exp((i - midp) / sf))
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
    
def proj_filter(raw, smooth, mid, steep):
    medf = nd.median_filter(raw, smooth)
    fns = sigmoidal_trans(mid, steep)
    thresh = apply_transfer_fn(medf, fns)
    return thresh

def main():
    #filename = 'output/surface-g3d-30-30-7.png'
    try:
        filename = sys.argv[1]
    except IndexError:
        print "Usage: %s filename" % (os.path.basename(sys.argv[0]))
        sys.exit(1)

    raw = scipy.misc.imread(filename)
    numpy_draw_pil(raw)

    #print_transfer_fn(fns)
    #sys.exit(0)

    #fn = gen_transfer_fn()
    #print_transfer_fn(fn)
    
    #medf = nd.median_filter(raw, 3)
    #numpy_draw_pil(medf)

    #fns = sigmoidal_trans(60, 15)
    #thresh = apply_transfer_fn(medf, fns)
    thresh = proj_filter(raw, 3, 60, 15)
    numpy_draw_pil(thresh)

    #alpha = 1
    #fl = nd.gaussian_filter(raw, 1.0)
    #sharpened = thresh + alpha * (thresh - fl)
    #numpy_draw_pil(sharpened)

    #alpha = 1
    #fl = nd.gaussian_filter(thresh, 3.0)
    #sharpened = thresh + alpha * (thresh - fl)
    #numpy_draw_pil(sharpened)

if __name__ == "__main__":
    main()
