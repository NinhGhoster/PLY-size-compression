# PLY Size Compression Benchmarks

A comprehensive toolkit and benchmarking suite dedicated to effectively compressing large 3D PLY datasets while strictly tracking geometry performance, mathematical data preservation (lossless vs. lossy), and direct software readability.

---

## 📂 Repository Structure

The repository has been organized to keep raw data, treated outputs, and processing scripts cleanly separated:

- **`data/original_meshes/`**  
  Contains the raw, untreated ASCII `.ply` models (typically 20MB–40MB each).
- **`data/benchmark_outputs/`**  
  Contains the results of various compression techniques (e.g., `.gz` archives, `.vtp` formats, `.drc` files, and `.ply` binary forms).
- **`scripts/`**  
  Contains all Python benchmarking scripts used to generate the data compression variants (`trimesh`, `VTK`, `Open3D`, etc.).

---

## 📊 Quick Comparison Matrix

Not all compression is equal. If you compress a file using `GZIP` or `7-Zip/LZMA`, standard 3D tracking software (like MeshLab, Blender, Unity) **cannot** read it out-of-the-box without manual unzipping. 

The table below breaks down every method we tested on a standard `21.14 MB` sample mesh based on performance, data integrity, and direct software compatibility.

| Methodology | File Size | Space Saved | Data Quality | Directly Readable? | Output Format |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Raw ASCII PLY (Baseline)** | `21.14 MB` | 0% | 100% Lossless | **Yes** | `.ply` |
| **Compact Binary PLY** | `16.10 MB` | ~24%| 100% Lossless | **Yes** (Best for direct use) | `.ply` |
| **Trimmed Binary PLY** | `16.08 MB` | ~24%| Semi-Lossless | **Yes** | `.ply` |
| **Precision Trimmed + GZIP** | `10.05 MB` | ~52%| Semi-Lossless | **No** (Needs unzip) | `.ply.gz` |
| **7-Zip (LZMA)** | `10.12 MB` | ~52%| 100% Lossless | **No** (Needs unzip) | `.7z` / `.xz` |
| **GZIP Archiver** | `14.71 MB` | ~30%| 100% Lossless | **No** (Needs unzip) | `.gz` |
| **VTK Native Zlib (PolyData)** | `19.85 MB` | ~6% | 100% Lossless | **Yes*** (Only in VTK viewers) | `.vtp` |
| **Google Draco** | `0.91 MB` | ~95%| Lossy (Quantized)| **Yes*** (Needs Draco plugin) | `.drc` |

> *Note: "Semi-Lossless" (Visually Identical) means microscopic mathematical precision (e.g., `1.512948...`) was truncated strictly to millimeter accuracy (e.g., `1.513`). This physically preserves visual mesh structure perfectly, but saves vast amounts of textual footprint.*

---

## 🚀 Key Takeaways & Recommendations

If you're unsure which method to use for your specific workflow, here is a quick guide outlining the best path forward:

### 1. Direct Software Readability (The Winner)
If you require files to be **drag-and-drop ready** for standard 3D software (Blender, Unity, MeshLab) with zero extraction required:
👉 Use **Compact Binary PLY**. It reliably shrinks the 21 MB ASCII footprint down to **16 MB** (24% reduction) by compiling strings into raw machine bytes. It is 100% mathematically lossless and universally supported.

### 2. Archival Cold Storage
If you are moving files to an external hard drive for backup or transferring massive datasets securely via the web (where strict 100% geometrical preservation is required):
👉 Use **LZMA (7-Zip)**. It aggressively crushes complex geometric float patterns significantly better than standard GZIP, taking the 21 MB payload natively down to **10 MB** (52% reduction) flawlessly.

### 3. Lightweight Web & Realtime Engines
If strictly lossless mathematical geometry is not required (e.g. visual-only rendering, video games, or web hosting):
👉 Use **Google Draco**. It employs heavy floating-point quantization to practically eliminate the storage footprint, resulting in a staggering **0.91 MB** (~95% reduction) visually-lossless scan.

---

## 💻 Getting Started (Running the Scripts)

To replicate these benchmark compressions on your own models using the provided scripts:

1. Create a Python Virtual Environment:
```bash
python3 -m venv venv
source venv/bin/activate
```
2. Install the necessary geometry processing dependencies:
```bash
pip install trimesh numpy vtk meshoptimizer open3d dracopy
```
3. Run any specialized script on a target `.ply` model:
```bash
python scripts/advanced_compression.py "data/original_meshes/0609_06_mesh_1.ply"
```
