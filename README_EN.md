
# pytorch3d Installation
```bash
pip3 install torch torchvision torchaudio
pip install https://github.com/facebookresearch/pytorch3d/archive/main.zip
```

# 2D Technical Drawing to 3D Model Generation Project

This project is an advanced computer vision and 3D modeling system that automatically generates 3D models from 2D technical drawings.

## 🎯 Project Summary

The system detects geometric shapes and holes in technical drawings using image processing techniques, contour analysis, and voxel-based 3D reconstruction algorithms, and then converts them into 3D mesh models.

## 🚀 Features

- ✅ **Automatic Main Shape Detection**: Accurate contour selection using hierarchy analysis  
- ✅ **Hole Detection**: Automatic recognition of nested hole structures  
- ✅ **3D Transformation**: Real 3D model generation using a voxel-based system  
- ✅ **Interactive Visualization**: View and inspect 3D models with Open3D  
- ✅ **Multi-Format Support**: PNG, JPEG, JPG file support  
- ✅ **Debug Mode**: Visual step-by-step process tracking  

## 📋 Requirements

```bash
pip install opencv-python
pip install open3d
pip install numpy
pip install scikit-image
pip install reportlab  # For report generation
```

## 🛠️ Installation

1. Clone the repository:
```bash
git clone <repo-url>
cd 2D-to-3D
```

2. Install required libraries:
```bash
pip install -r requirements.txt
```

## 📖 Usage

### Basic Usage

```python
from technical_drawing_to_3d import TechnicalDrawingTo3D

# Load a 2D technical drawing and convert it to 3D
converter = TechnicalDrawingTo3D("path/to/your/drawing.png")
mesh = converter.process()
```

### Run from CLI

```bash
python technical_drawing_to_3d.py
```

## 🏗️ System Architecture

### Core Components

| Component | File | Description |
|----------|------|-------------|
| `TechnicalDrawingProcessor` | `technical_drawing_processor.py` | Image processing and contour detection |
| `TechnicalDrawingTo3D` | `technical_drawing_to_3d.py` | 3D mesh generation and visualization |

### Workflow

```
Image Loading → Preprocessing → Threshold Analysis → Contour Detection →  
Hierarchy Analysis → Main Shape Selection → Hole Detection → Voxel Grid →  
Marching Cubes → 3D Mesh → Visualization
```

## 🔬 Technical Details

### Image Processing Algorithms

- **Multi-Thresholding**: [50, 100, 127, 150, 200] + Otsu  
- **Hierarchical Contour Analysis**: OpenCV RETR_TREE mode  
- **Advanced Contour Selection**: Based on area ratio and parent-child relationship analysis  

### 3D Reconstruction

- **Voxel Grid**: Shape of (height, width, 100)  
- **Marching Cubes**: Mesh generation with level 0.5  
- **Coordinate Transformation**: Centering and 200-unit normalization  

## 📊 Test Results

Test results from the latest run:

| Metric | Value | Description |
|--------|-------|-------------|
| Main Contour Area | 72,925.5 pixels | Accurate main shape detection |
| Detected Holes | 2 holes | Success of hierarchy analysis |
| Voxel Ratio | 13.2% material, 86.8% hole | Realistic material usage |
| Final Mesh | 183,800 vertices, 363,924 faces | High-quality mesh |
| Processing Time | ~3–5 seconds | Fast processing |

## 🐛 Debug Files

The system generates visual debug files during processing:

- `debug_thresh_X_normal.png`: Normal binary at threshold X  
- `debug_thresh_X_inv.png`: Inverted binary at threshold X  
- `debug_final_binary.png`: Final selected binary image  
- `debug_final_contours.png`: Main shape (green) + holes (blue)  
- `debug_corrected_mask.png`: Final profile mask  

## 📈 Development Process

### Key Problems Solved

1. **Incorrect Contour Selection** → Fixed with hierarchy + area ratio analysis  
2. **Invisible Holes** → Solved with voxel-level masking  
3. **Boolean Logic Failures** → Replaced with voxel-based operations  
4. **Threshold Issues** → Introduced multi-threshold test algorithm  

### Iterative Development Versions

1. **V1**: Simple thresholding + basic contour detection  
2. **V2**: Parallel line detection (later removed)  
3. **V3**: Simplified to pure contour analysis  
4. **V4**: Hierarchical contour analysis  
5. **V5**: Multi-threshold testing system  
6. **V6**: Improved contour selection algorithm  
7. **Final**: Voxel-based hole carving system  

## 📝 License

This project is licensed under the MIT License.

## 🤝 How to Contribute?

1. Fork the repo and create your own copy  
2. Create a new branch (`feature/xyz`)  
3. Make your changes  
4. Submit a pull request (PR)  

## 📐 Code Guidelines

- Add meaningful comments to your code  
- Keep changes aligned with the project's structure  
- Include test files if applicable  

## 📫 Contact

For questions or suggestions, feel free to open an issue or contact me directly:  
📧 hamzaebrarguner@gmail.com

## 👨‍💻 Developer Info

**2D-to-3D Technical Drawing Converter**  
- Developed in: 2025  
- Technologies: Python, OpenCV, Open3D, NumPy, scikit-image
