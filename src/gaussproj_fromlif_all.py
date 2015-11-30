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
from gaussproj import flush_message
import proj
 

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
		print "Usage: %s lif_directory [sdx] [sdy] [sdz]" % os.path.basename(sys.argv[0])
		sys.exit(1)
		
	try:
            sdx, sdy, sdz = int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
        except IndexError:
            print "Using default values for standard deviation"
            sdx, sdy, sdz = 4, 4, 3
		
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
		
		#sdx, sdy, sdz = 4, 4, 3
		sds = 4
	
		output_dir = "./proj_%s_%s" % (lifdir, im_num)
	
		if not os.path.exists(output_dir):
			os.makedirs(output_dir)
		
		max_proj = np.amax(ma, axis=2)
		
		mpfilename = os.path.join(output_dir, "max-proj.png")
		scipy.misc.imsave(mpfilename, max_proj)
		
		bl = nd.gaussian_filter(ma, [sdx, sdy, sdz])

		#ps = find_projection_surface(bl)
		ps = proj.max_indices_z(bl)

		sps = nd.gaussian_filter(ps, sds)
		
		vis_factor = 255 / z_size
		sfilename = os.path.join(output_dir, "surface-g3d-%d-%d-%d-%d.png" % (sdx, sdy, sdz, sds))
		scipy.misc.imsave(sfilename, sps * vis_factor)

		res = proj.projection_from_surface(ma, sps, dm=3, dp=0)

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
