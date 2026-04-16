import vtk
import os
import sys

input_file = sys.argv[1]

# Read PLY
reader = vtk.vtkPLYReader()
reader.SetFileName(input_file)
reader.Update()
polydata = reader.GetOutput()

# Write VTP with ZLib Compression
vtp_file = input_file.replace(".ply", ".vtp")
writer = vtk.vtkXMLPolyDataWriter()
writer.SetFileName(vtp_file)
writer.SetInputData(polydata)
writer.SetDataModeToAppended()
writer.SetCompressorTypeToZLib()
writer.Write()

# Write VTK Binary PLY
ply_bin_file = input_file.replace(".ply", "_vtkBinary.ply")
ply_writer = vtk.vtkPLYWriter()
ply_writer.SetFileName(ply_bin_file)
ply_writer.SetInputData(polydata)
ply_writer.SetFileTypeToBinary()
ply_writer.Write()

print(f"[VTK VTP ZLib Lossless Compressed] Size: {os.path.getsize(vtp_file) / (1024*1024):.2f} MB")
print(f"[VTK PLY Binary] Size: {os.path.getsize(ply_bin_file) / (1024*1024):.2f} MB")
