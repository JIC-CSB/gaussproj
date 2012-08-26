#!/usr/bin/env python
import vtk

print "Loading data...",
#reader = vtk.vtkXMLImageDataReader()
reader = vtk.vtkPNGReader()

arr = vtk.vtkStringArray()
arr.InsertNextValue('data/pngstack/ExpID3002_spch4_TL003_plantD_lif_S000_T000_C000_Z018.png')
arr.InsertNextValue('data/pngstack/ExpID3002_spch4_TL003_plantD_lif_S000_T000_C000_Z019.png')
arr.InsertNextValue('data/pngstack/ExpID3002_spch4_TL003_plantD_lif_S000_T000_C000_Z020.png')
arr.InsertNextValue('data/pngstack/ExpID3002_spch4_TL003_plantD_lif_S000_T000_C000_Z021.png')
arr.InsertNextValue('data/pngstack/ExpID3002_spch4_TL003_plantD_lif_S000_T000_C000_Z022.png')
arr.InsertNextValue('data/pngstack/ExpID3002_spch4_TL003_plantD_lif_S000_T000_C000_Z023.png')
arr.InsertNextValue('data/pngstack/ExpID3002_spch4_TL003_plantD_lif_S000_T000_C000_Z024.png')
arr.InsertNextValue('data/pngstack/ExpID3002_spch4_TL003_plantD_lif_S000_T000_C000_Z025.png')

reader.SetFileNames(arr)
reader.SetDataSpacing(0.305, 0.305, 0.987)
reader.Update()
data = reader.GetOutput()
data.SetExtent(0, 50, 0, 50, 0, 5)
#data.SetScalarTypeToUnsignedChar()

print "...done"

volumeMapper = vtk.vtkVolumeRayCastMapper()
volumeMapper.SetInput(data)

volume = vtk.vtkVolume()
volume.SetMapper(volumeMapper)

ren = vtk.vtkRenderer()
ren.AddVolume(volume)
renWin = vtk.vtkRenderWindow()

#iact = vtk.vtkImageActor()
#iact.SetInput(data)
#ren.AddActor(iact)

renWin.SetSize(1024,768)
renWin.AddRenderer(ren)
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)
iren.Initialize()
renWin.Render()
iren.Start()
