#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  gaussproj_fromlif.py
#  
#  Copyright 2015 Ross Carter (JIC) <carterr@n108308.nbi.ac.uk>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#


"""
Does exactly the same as Gaussproj but takes a lif file as input
and projects all images in stack

Usage: python gaussproj_fromlif_all lif_file

saves output in ./output_lif file_image number
"""

import sys, os
import numpy as np
import javabridge
import bioformats as bf
from pylab import imshow, show
from xml import etree as et
import matplotlib.pyplot as plt
from gaussproj import *
 

def parse_xml_metadata(xml_string, array_order='zyx'):
    """Get interesting metadata from the LIF file XML string.
    Parameters
    ----------
    xml_string : string
        The string containing the XML data.
    array_order : string
        The order of the dimensions in the multidimensional array.
        Valid orders are a permutation of "tzyxc" for time, the three
        spatial dimensions, and channels.
    Returns
    -------
    names : list of string
        The name of each image series.
    sizes : list of tuple of int
        The dimensions of the image in the specified order of each image.
    resolutions : list of tuple of float
        The resolution of each series in the order given by
        `array_order`. Time and channel dimensions are ignored.
    """
    array_order = array_order.upper()
    names, sizes, resolutions = [], [], []
    spatial_array_order = [c for c in array_order if c in 'XYZ']
    size_tags = ['Size' + c for c in array_order]
    res_tags = ['PhysicalSize' + c for c in spatial_array_order]
    metadata_root = et.ElementTree.fromstring(xml_string)
    for child in metadata_root:
        if child.tag.endswith('Image'):
            names.append(child.attrib['Name'])
            for grandchild in child:
                if grandchild.tag.endswith('Pixels'):
                    att = grandchild.attrib
                    sizes.append(tuple([int(att[t]) for t in size_tags]))
                    resolutions.append(tuple([float(att[t]) for t in res_tags]))
    return names, sizes, resolutions

def vis2d(ma, sps, indices, axis=1, d=-3, aspect=1, threshold=10):
    N = len(indices)
    if axis==1:
        plt.figure(figsize=(2*N, 15))
    else:
        plt.figure(figsize=(12, 2*N))
    N = len(indices)
    for i, idx in enumerate(indices):
        s = np.take(ma, idx, axis)
        h = np.take(sps, idx, axis)
        if axis==1:
            plt.subplot(1, N, i+1)
            plt.imshow(np.minimum(threshold, s), cmap=plt.cm.gray, aspect=1.0/aspect)
            plt.hold(True)
            plt.plot(h, range(ma.shape[0]), 'r')
            plt.plot(np.clip(h+d, 0, ma.shape[2]-1), range(ma.shape[0]), 'g')
            plt.ylim(0, ma.shape[0])
            plt.xlim(0, ma.shape[2])
            plt.xticks([])
            if i>0:
                plt.yticks([])
        else:
            plt.subplot(N, 1, i+1)
            plt.imshow(np.minimum(threshold, s.T), cmap=plt.cm.gray, aspect=aspect)
            plt.hold(True)
            plt.plot(range(ma.shape[1]), h, 'r')
            plt.plot(range(ma.shape[1]), np.clip(h+d, 0, ma.shape[2]-1), 'g')
            plt.xlim(0, ma.shape[1])
            plt.ylim(ma.shape[2], 0)
            plt.yticks([])
            if i>0:
                plt.xticks([])

def greyScale(image):
	""" Converts RGB to greyscale as Y = 0.299R + 0.587G + 0.144B """
	
	flush_message("Converting to greyscale...")
	grey = np.dot(image[...,:3], [0.299, 0.587, 0.144])
	print "done"
	return grey
			
def main(args):
	javabridge.start_vm(class_path=bf.JARS)
	
	try:
		lifdir = sys.argv[1]
	except IndexError:
		print "Usage: %s lif_directory " % os.path.basename(sys.argv[0])
		sys.exit(1)
		
	md = bf.get_omexml_metadata(lifdir)
	mdo = bf.OMEXML(md)	
	rdr = bf.ImageReader(lifdir, perform_init=True)
	
	
	names, sizes, resolutions = parse_xml_metadata(md)
	
	
	print '%s contains:' % lifdir
	for i in range(mdo.image_count):
		print '%d, %s, %s' % (i,names[i],(sizes[i],))
	
	
	
	for im_num in range(mdo.image_count):
		im_size = ()
		im_size = [sizes[im_num][1],sizes[im_num][2],sizes[im_num][0],3]
	
		image3d = np.empty(im_size, np.uint8)
		print 'projecting: %d, %s, %s' % (im_num,names[im_num],(sizes[im_num],))
		
		z_size = sizes[im_num][0]
		
		flush_message('Importing...')
		for z in range(z_size):
			image3d[:,:,z,:] = rdr.read(z=z, series=im_num, rescale=False)
		print 'done'

		#ma = greyScale(image3d)
		ma = np.amax(image3d, 3)
		
		sdx, sdy, sdz = 4, 4, 3
		sds = 4
	
		output_dir = "./proj_%s_%s" % (lifdir, im_num)
	
		if not os.path.exists(output_dir):
			os.makedirs(output_dir)
		
		max_proj = np.amax(ma, axis=2)
		
		mpfilename = os.path.join(output_dir, "max-proj.png")
		save_numpy_as_png(mpfilename, max_proj)
		
		bl = apply_gaussian_filter(ma, [sdx, sdy, sdz])

		#ps = find_projection_surface(bl)
		ps = np.argmax(bl, 2)

		sps = nd.gaussian_filter(ps, sds)
		
		vis_factor = 255 / z_size
		sfilename = os.path.join(output_dir, "surface-g3d-%d-%d-%d-%d.png" % (sdx, sdy, sdz, sds))
		save_numpy_as_png(sfilename, sps * vis_factor)

		res = projection_from_surface(ma, sps)

		filename = os.path.join(output_dir, "proj-g3d-%d-%d-%d-%d.png" % (sdx, sdy, sdz, sds))
		pmax = np.amax(res)

		vis_scale = 255 / pmax

		scipy.misc.imsave(filename, res * vis_scale)

		flush_message("Post processing...")
		pp = projpp.proj_filter(res * vis_scale, 3, 60, 15)
		print " done"
		filename = os.path.join(output_dir, 'proj-pp-%d-%d-%d-%d.png' % (sdx, sdy, sdz, sds))
		scipy.misc.imsave(filename, pp)
	
	javabridge.kill_vm()
	return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
