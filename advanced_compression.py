import sys
import os
import trimesh
import numpy as np

def process_mesh(input_file):
    print(f"Loading {input_file}...")
    mesh = trimesh.load(input_file)
    
    # --- Semi-Lossless Precision Trimming ---
    # Round to 3 decimal places (millimeter accuracy if in meters)
    mesh.vertices = np.round(mesh.vertices, 3)
    out_trimmed = input_file.replace(".ply", "_precision_trimmed.ply")
    mesh.export(out_trimmed, file_type='ply', encoding='ascii')
    
    print(f"Generated {out_trimmed} (Trimmed Precision)")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        process_mesh(sys.argv[1])
