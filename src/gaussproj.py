#!/usr/bin/env python2.7

#import matplotlib
import numpy as np
#import imread
#import Image
#from matplotlib import pyplot as plt
import itertools
import scipy
import scipy.ndimage as nd
import sys

def numpy_draw_pyplot(r):
    plt.imshow(r, interpolation='nearest')
    plt.show()

def numpy_draw_pil(r):
    i = Image.fromarray(r)
    i.show()

def read_and_conv(filename):
    na = scipy.misc.imread(filename)
    #na = imread.imread(filename)
    return na[:,:,0]

def load_png_stack(impattern, istart, iend):
    flush_message("Loading images...")
    ifiles = [impattern % i for i in range(istart, iend)]
    ma = np.dstack(itertools.imap(read_and_conv, ifiles))
    print " done, array is", ma.shape
    return ma

def flush_message(message):
    print message,
    sys.stdout.flush()

def apply_gaussian_filter(ma, sd):
    flush_message("Applying 3D gaussian filter...")
    bl = nd.gaussian_filter(ma, sd)
    print " done"
    return bl

def get_max(bl, x, y):
    dp = list(bl[x, y, :])
    return dp.index(max(dp))

def find_projection_surface(bl):
    flush_message("Finding projection surface...")
    xmax, ymax, zmax = bl.shape
    surface = np.zeros([xmax, ymax], dtype=np.uint8)
    for x in range(0, xmax):
        for y in range(0, ymax):
            z = get_max(bl, x, y)
            surface[x, y] = z
            #res[x, y] = ma[x, y, z]
    print " done"
    return surface

def projection_from_surface(ma, surface):
    flush_message("Generating projection from surface...")
    xmax, ymax, zmax = ma.shape
    res = np.zeros([1024, 1024], dtype=np.uint8)
    for x in range(0, xmax):
        for y in range(0, ymax):
            z = surface[x, y]
            res[x, y] = ma[x, y, z]
    print " done"
    return res

def save_numpy_as_png(filename, np):
    scipy.misc.imsave(filename, np)

def main():

    impattern = 'data/pngstack/ExpID3002_spch4_TL003_plantD_lif_S000_T000_C000_Z0%02d.png'
    istart = 6
    iend = 92

    try:
        sdx, sdy, sdz = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    except IndexError:
        print "Using default values for standard deviation"
        sdx, sdy, sdz = 25, 25, 7

    print "Using standard deviations: %d, %d, %d" % (sdx, sdy, sdz)

    ma = load_png_stack(impattern, istart, iend)

    bl = apply_gaussian_filter(ma, [sdx, sdy, sdz])

    ps = find_projection_surface(bl)
    sfilename = "output/surface-g3d-%d-%d-%d.png" % (sdx, sdy, sdz)
    save_numpy_as_png(sfilename, ps)

    res = projection_from_surface(ma, ps)
    filename = "output/proj-g3d-%d-%d-%d.png" % (sdx, sdy, sdz)
    scipy.misc.imsave(filename, res)

    #numpy_draw_pil(res)

if __name__ == "__main__":
    main()
