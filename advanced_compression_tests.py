import sys
import os
import trimesh
import numpy as np
import meshoptimizer
import lzma
import gzip

def get_size_mb(path):
    return os.path.getsize(path) / (1024*1024)

def process_tests(input_file):
    print(f"Loading {input_file} for tests...")
    # Baseline
    print(f"Original size: {get_size_mb(input_file):.2f} MB")
    with open(input_file, "rb") as f: orig_data = f.read()
    
    # Baseline GZIP (we know this is ~14.71 MB)
    gz_orig = input_file + ".gz"
    with open(gz_orig, "wb") as f: f.write(gzip.compress(orig_data))
    print(f"Baseline GZIP: {get_size_mb(gz_orig):.2f} MB")
    
    # 2. LZMA Compression
    lzma_file = input_file + ".xz"
    with lzma.open(lzma_file, "w", preset=9) as f: f.write(orig_data)
    print(f"[Option 2: LZMA / 7-Zip Algorithm] Size: {get_size_mb(lzma_file):.2f} MB")

    # Load Mesh
    mesh = trimesh.load(input_file)
    original_vertices = mesh.vertices.shape[0]
    indices_flat = mesh.faces.flatten().astype(np.uint32)
    
    # 1. Spatial Reordering
    faces_opt_flat = meshoptimizer.optimize_vertex_cache(indices_flat, original_vertices)
    vertices_opt, faces_fetch_flat = meshoptimizer.optimize_vertex_fetch(mesh.vertices, faces_opt_flat)
    faces_fetch = faces_fetch_flat.reshape(-1, 3)
    
    mesh_sorted = trimesh.Trimesh(vertices=vertices_opt, faces=faces_fetch)
    out_sorted = input_file.replace(".ply", "_spatially_sorted.ply")
    mesh_sorted.export(out_sorted, file_type='ply', encoding='ascii')
    with open(out_sorted, "rb") as f: sorted_data = f.read()
    
    gz_sorted = out_sorted + ".gz"
    with open(gz_sorted, "wb") as f: f.write(gzip.compress(sorted_data))
    print(f"[Option 1: Spatial Reordering + GZIP] Size: {get_size_mb(gz_sorted):.2f} MB")
    
    # 3. Precision Trimming (Visually Lossless)
    mesh_trimmed = trimesh.Trimesh(vertices=np.round(mesh.vertices, 3), faces=mesh.faces)
    out_trimmed = input_file.replace(".ply", "_precision_trimmed.ply")
    mesh_trimmed.export(out_trimmed, file_type='ply', encoding='ascii')
    with open(out_trimmed, "rb") as f: trimmed_data = f.read()
    
    gz_trimmed = out_trimmed + ".gz"
    with open(gz_trimmed, "wb") as f: f.write(gzip.compress(trimmed_data))
    print(f"[Option 3: Precision Trimming + GZIP] Size: {get_size_mb(gz_trimmed):.2f} MB")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        process_tests(sys.argv[1])
