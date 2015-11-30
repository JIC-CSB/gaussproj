#!/usr/bin/env python2.7

"""
gaussproj - A simple script to project (single channel) three-dimensional
image stacks onto two dimensional surfaces
"""

import itertools, sys, os
import scipy
import scipy.ndimage as nd
import numpy as np
import stackhandle
import projpp
import proj

def read_and_conv(filename):
    try:
        na = scipy.misc.imread(filename)
    except IOError, e:
        print "ERROR: couldn't open %s" % filename
        print e
        sys.exit(1)

    #TODO - nicer way of doing this

    try:
        x, y, z = na.shape
    except ValueError:
        return na

    return np.amax(na, 2)

def load_png_stack(ifiles):
    flush_message("Loading images...")

    ma = np.dstack(itertools.imap(read_and_conv, ifiles))
    print " done, array is", ma.shape
    return ma

def flush_message(message):
    print message,
    sys.stdout.flush()


def main():
    try:
        stackdir = sys.argv[1]
    except IndexError:
        print "Usage: %s stack_dir [output_dir] [sdx] [sdy] [sdz]" % os.path.basename(sys.argv[0])
        sys.exit(1)

    ifiles = stackhandle.get_stack_files(stackdir)

    try:
        output_dir = sys.argv[2]
    except IndexError:
        output_dir = 'output/'
        print "Using default output directory output/"

    print "Called with", stackdir, output_dir

    try:
        sdx, sdy, sdz = int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
    except IndexError:
        print "Using default values for standard deviation"
        sdx, sdy, sdz = 8, 8, 6

    sds = 5

    print "Using standard deviations: %d, %d, %d" % (sdx, sdy, sdz)

    ma = load_png_stack(ifiles)

    flush_message("Applying 3D gaussian filter...")
    bl = nd.gaussian_filter(ma, [sdx, sdy, sdz])
    print "done"

    flush_message("Finding projection surface...")
    ps = proj.max_indices_z(bl)
    print "done"

    sps = nd.gaussian_filter(ps, sds)
    _, _, zmax = ma.shape
    vis_factor = 255 / zmax
    sfilename = os.path.join(output_dir, "surface-g3d-%d-%d-%d-%d.png" % (sdx, sdy, sdz, sds))
    scipy.misc.imsave(sfilename, sps * vis_factor)

    flush_message("Generating projection from surface...")
    res = proj.projection_from_surface_z(ma, sps, dm=3, dp=0) 
    print "done"

    filename = os.path.join(output_dir, "proj-g3d-%d-%d-%d-%d.png" % (sdx, sdy, sdz, sds))
    pmax = np.amax(res)
    vis_scale = 255 / pmax
    scipy.misc.imsave(filename, res * vis_scale)

    flush_message("Post processing...")
    pp = projpp.proj_filter(res * vis_scale, 3, 60, 15)
    print "done"

    filename = os.path.join(output_dir, 'proj-pp-%d-%d-%d-%d.png' % (sdx, sdy, sdz, sds))
    scipy.misc.imsave(filename, pp)


if __name__ == "__main__":
    main()
