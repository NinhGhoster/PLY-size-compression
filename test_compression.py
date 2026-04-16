import sys
import os
import open3d as o3d
import meshio
import DracoPy

def test_compression(input_file):
    print(f"--- Testing Compression Methods on {input_file} ---")
    orig_size = os.path.getsize(input_file)
    print(f"Original size: {orig_size / (1024*1024):.2f} MB")
    
    # Method 1: Binary PLY
    out_ply = input_file.replace(".ply", "_binary.ply")
    mesh_o3d = o3d.io.read_triangle_mesh(input_file)
    o3d.io.write_triangle_mesh(out_ply, mesh_o3d, write_ascii=False)
    ply_size = os.path.getsize(out_ply)
    print(f"[Open3D Binary] Size: {ply_size / (1024*1024):.2f} MB")
    
    print("[OpenCTM] Meshio does not support exporting to .ctm natively.")
    mesh_meshio = meshio.read(input_file)

    
    # Method 3: DracoPy
    out_drc = input_file.replace(".ply", ".drc")
    faces = []
    for cell in mesh_meshio.cells:
        if cell.type == "triangle":
            faces = cell.data
            break
            
    draco_data = DracoPy.encode(mesh_meshio.points, faces, compression_level=10)
    with open(out_drc, "wb") as f:
        f.write(draco_data)
    drc_size = os.path.getsize(out_drc)
    print(f"[Draco] Size: {drc_size / (1024*1024):.2f} MB")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        test_compression(sys.argv[1])
    else:
        print("Please provide a file.")
