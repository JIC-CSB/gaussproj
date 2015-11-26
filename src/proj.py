#!/usr/bin/env python2.7

import scipy
import scipy.ndimage as nd
import numpy as np
from math import sqrt
import numpy.linalg as la

# Methods for simple projection in the z-direction

def max_indices_z(A, clip_bottom=True):
    h = np.argmax(A, 2)
    if clip_bottom:
        h[np.logical_and(h==0, A[:,:,0]==A[:,:,-1])] = A.shape[2]-1
    return h

def threshold_indices_z(A, b, c, clip_bottom=True):
    t = b*np.mean(A, axis=2) + c
    # now wish to find first occurance
    return max_indices_z(A > t[:,:, np.newaxis], clip_bottom)


def sheet_indices_z(I, niter=1000, dt=0.05, a=3.0, b=3.0):
    h0 = np.zeros(I.shape[0:2])
    i, j = np.meshgrid(np.arange(I.shape[0]), np.arange(I.shape[1]), order='ij')
    d2 = np.zeros(h0.shape)
    for k in range(niter):
        d2[1:-1, 1:-1] = h0[:-2, 1:-1]+ h0[2:,1:-1] + h0[1:-1,:-2] + h0[1:-1,2:] - 4*h0[1:-1, 1:-1]
        I_h = I[i.T, j.T, h0.astype(int)]
        h0 += dt/(1+b*I_h) + d2*a*dt
        h0 = np.clip(h0, 0, I.shape[2]-1)
    return h0    


def projection_from_surface_z(ma, surface, dm=0, dp=10, op=np.max):
    xmax, ymax, zmax = ma.shape
    res = np.zeros([xmax, ymax], dtype=ma.dtype)
    z0 = np.clip(surface-dm, 0, zmax-1).astype(int)
    z1 = np.clip(surface+dp, 1, zmax).astype(int)
    for x in range(0, xmax):
        for y in range(0, ymax):
            res[x, y] = op(ma[x, y, z0[x,y]:z1[x,y]])
    return res

def projection_from_surface_normal_z(ma, surface, dm=0, dp=10, 
                                        op=np.max, gradient_radius=0.5):
    imax, jmax, kmax = ma.shape
    res = np.zeros([imax, jmax], dtype=ma.dtype)
    surface_di = scipy.ndimage.gaussian_filter1d(surface, 0.5, axis=0, order=1)
    surface_dj = scipy.ndimage.gaussian_filter1d(surface, 0.5, axis=1, order=1)

    def clip(i_,j_,k_):
        return np.array( (max(0, min(i_, imax-1)), max(0, min(j_, jmax-1)), max(0, min(k_, kmax-1))) )
    
    for i in range(0, imax):
        for j in range(0, jmax):
            si = -surface_di[i,j]
            sj = -surface_dj[i,j]
            k = surface[i,j]
            sk = 1.0
            h = sqrt(si*si+sj*sj+sk*sk)
            si = si/h
            sj = sj/h
            sk = sk/h
            p_start = clip(i-dm*si, j-dm*sj, k-dm*sk)
            p_end = clip(i+dp*si, j+dp*sj, k+dp*sk)
            ns = int(la.norm(p_end-p_start) +1)
            tt = np.linspace(0, 1, ns)
            res[i,j] = op( scipy.ndimage.map_coordinates(ma, 
                            ([(p_start[0]*(1-t) + p_end[0]*t) for t in tt],
                             [(p_start[1]*(1-t) + p_end[1]*t) for t in tt],
                             [(p_start[2]*(1-t) + p_end[2]*t) for t in tt]),
                                                         order=1 ))
    return res





