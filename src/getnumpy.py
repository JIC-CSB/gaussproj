#!/usr/bin/env python

import vtk
from numpy import *
import os

reader = vtk.vtkPNGReader()

arr = vtk.vtkStringArray()

fpath = 'data/pngstack'

files = os.listdir('data/pngstack')

limit = 5

for i in range(0, limit):
    arr.InsertNextValue(os.path.join(fpath, files[i]))

reader.SetFileNames(arr)
reader.SetDataSpacing(0.305, 0.305, 0.987)
reader.Update()
data = reader.GetOutput()
data.SetExtent(0, 500, 0, 500, 0, limit)

for x in range(0, 50):
    for y in range(0, 50):
        print data.GetScalarComponentAsFloat(x, y, 0, 0)
