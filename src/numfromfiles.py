#!/opt/local/bin/python2.7

#import matplotlib
import numpy as np
import imread

imfile ='data/pngstack/ExpID3002_spch4_TL003_plantD_lif_S000_T000_C000_Z006.png'
imfile2 ='data/pngstack/ExpID3002_spch4_TL003_plantD_lif_S000_T000_C000_Z007.png'

#na = matplotlib.pyplot.imread(imfile)

def stuffwithpng():

    r = png.Reader(imfile)
    
    x, y, pd, info = r.asDirect()
    
    print "PD", pd
    
    def rgb_to_uint8(r, g, b):
        return r
    
    #for a in pd:
    #    print a

na = imread.imread(imfile)

r = na[:,:,0]

na2 = imread.imread(imfile2)

r2 = na2[:, :, 0]

ma = np.dstack([r, r2])

print ma.shape

