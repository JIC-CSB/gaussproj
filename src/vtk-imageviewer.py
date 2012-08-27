#!/usr/bin/env python

import vtk

def ipip_imagename():
    return "ExpID3002_spch4_TL004_plantD_cropped.png"

ren = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)


pngreader = vtk.vtkPNGReader()
pngreader.SetFileName(ipip_imagename())
pngreader.Update()
viewer = vtk.vtkImageViewer2()
viewer.SetInputConnection(pngreader.GetOutputPort())

imgActor = vtk.vtkImageActor()



iren = vtk.vtkRenderWindowInteractor()

viewer.SetupInteractor(iren)

viewer.Render()

iren.Initialize()
iren.Start()
