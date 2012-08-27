#!/usr/bin/env python2.7

import scipy.misc
import numpy as np

n0 = np.zeros([1024, 1024, 3], dtype = np.uint8)

scipy.misc.imsave('blank.png', n0)


