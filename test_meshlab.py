import sys
import os
import pymeshlab

input_file = sys.argv[1]

ms = pymeshlab.MeshSet()
# Load the original ASCII mesh
ms.load_new_mesh(input_file)

# Save the mesh (defaults to binary format for .ply in pymeshlab)
out_file = input_file.replace(".ply", "_meshlab.ply")
ms.save_current_mesh(out_file, save_face_color=True, save_vertex_color=True, save_vertex_normal=True, binary=True)

size_mb = os.path.getsize(out_file) / (1024*1024)
print(f"[MeshLab Binary PLY] Size: {size_mb:.2f} MB")
