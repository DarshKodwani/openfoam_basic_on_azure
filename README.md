# OpenFOAM Basic Tutorials on Azure

This repository provides a complete toolkit for setting up OpenFOAM on Azure (or any Ubuntu-based system) and running computational fluid dynamics (CFD) simulations. It includes installation scripts, tutorial execution, and Python-based visualization tools for analyzing OpenFOAM simulation results.

## 🎯 Purpose

This repository demonstrates how to:
- Set up OpenFOAM on a cloud environment (specifically Azure, but works on any Ubuntu system)
- Run the classic motorBike tutorial simulation
- Analyze and visualize CFD results using Python tools
- Create animations and detailed visualizations of fluid flow around complex geometries

## 📁 Repository Structure

### 🔧 Setup and Execution Scripts

#### `setup_openFOAM.sh`
**Purpose**: Automated installation script for OpenFOAM 10 and ParaView
**Usage**:
```bash
chmod +x setup_openFOAM.sh
./setup_openFOAM.sh
```
**What it does**:
- Updates system packages
- Adds OpenFOAM repository and GPG key
- Installs OpenFOAM 10 and ParaView
- Configures environment variables in `.bashrc`
- Sources OpenFOAM environment for immediate use

#### `run_motorbike_tutorial.sh`
**Purpose**: Executes the complete motorBike CFD simulation workflow
**Usage**:
```bash
# Ensure OpenFOAM is properly sourced first
source /opt/openfoam10/etc/bashrc
chmod +x run_motorbike_tutorial.sh
./run_motorbike_tutorial.sh
```
**What it does**:
- Creates a clean working directory in `~/openfoam-tests`
- Copies the motorBike tutorial from OpenFOAM installation
- Prepares geometry files (motorBike.obj)
- Runs the complete simulation pipeline:
  - `blockMesh`: Creates base mesh
  - `surfaceFeatures`: Extracts surface features
  - `snappyHexMesh`: Generates refined mesh around geometry
  - `simpleFoam`: Solves steady-state fluid flow
  - `foamToVTK`: Converts results to VTK format for visualization

### 🐍 Python Visualization Tools

#### `cfd_flow_animation.py`
**Purpose**: Creates comprehensive 4-panel animated visualizations of CFD results
**Requirements**:
```bash
pip install pyvista numpy
```
**Usage**:
```bash
python3 cfd_flow_animation.py
```
**Features**:
- **Panel 1**: Velocity field visualization with streamlines
- **Panel 2**: Pressure field distribution
- **Panel 3**: Motorbike geometry with surface mesh
- **Panel 4**: Advanced flow analysis (vorticity, flow separation)
- Creates rotating animations to show flow from multiple angles
- Generates high-quality renderings suitable for presentations

#### `motorbike_mesh_visualisation.py`
**Purpose**: Interactive mesh visualization with multiple viewing modes
**Usage**:
```bash
python3 motorbike_mesh_visualisation.py
```
**Features**:
- **Simple View**: Uniform coloring with edge visualization
- **Detailed View**: Color-coded parts with transparency
- **Exploded View**: Separated components for detailed inspection
- Interactive 3D viewing with mouse controls
- Part identification and inspection capabilities

### 📊 Example Output Data

#### `motorBike-VTK/` Directory
**Purpose**: Contains pre-computed simulation results for immediate visualization
**Contents**:
- `motorBike_*.vtk`: Volume mesh data at different time steps (0, 100, 200, 300, 400, 500 iterations)
- Individual component folders (e.g., `frontAndBack/`, `inlet/`, `motorBike_engine%56/`): Surface mesh data for specific motorbike parts
- Multiple geometry components: frame, wheels, engine, exhaust, rider, etc.

**Time Steps Available**:
- `_0.vtk`: Initial conditions
- `_100.vtk` to `_500.vtk`: Simulation progress at 100-iteration intervals

## 🚀 Quick Start Guide

### 1. Environment Setup
```bash
# Clone the repository
git clone <repository-url>
cd openfoam_basic_on_azure

# Install OpenFOAM (Ubuntu/Azure VM)
./setup_openFOAM.sh

# Restart terminal or source environment
source ~/.bashrc
```

### 2. Run Simulation
```bash
# Execute the complete motorBike tutorial
./run_motorbike_tutorial.sh
```

### 3. Visualize Results
```bash
# Install Python dependencies
pip install pyvista numpy

# Create animated flow visualization
python3 cfd_flow_animation.py

# Interactive mesh exploration
python3 motorbike_mesh_visualisation.py
```

## 📋 Prerequisites

- **System**: Ubuntu 18.04+ (or Azure Ubuntu VM)
- **Python**: 3.6+ with pip
- **Disk Space**: ~5GB for OpenFOAM installation + simulation data
- **Memory**: 4GB+ RAM recommended for visualization
- **Graphics**: OpenGL support for 3D visualization

## 🔬 Simulation Details

The motorBike tutorial demonstrates:
- **Flow Type**: Incompressible, steady-state turbulent flow
- **Solver**: simpleFoam (SIMPLE algorithm)
- **Geometry**: Complex 3D motorbike with rider
- **Mesh**: ~1.5M cells using snappyHexMesh
- **Boundary Conditions**:
  - Inlet: Uniform velocity (20 m/s)
  - Outlet: Zero pressure
  - Walls: No-slip condition
  - Motorbike surface: No-slip wall

## 🎨 Visualization Features

- **Velocity vectors and streamlines**
- **Pressure contours and gradients**
- **Surface mesh with edge highlighting**
- **Interactive 3D rotation and zooming**
- **Multi-panel comparative views**
- **Animation export capabilities**
- **Component-wise analysis**

## 📈 Expected Results

After running the simulation, you should observe:
- **Flow acceleration** over the motorbike body
- **Pressure reduction** in high-velocity regions
- **Wake formation** behind the motorbike
- **Boundary layer development** on surfaces
- **Vortex shedding** from sharp edges

## 🐛 Troubleshooting

**OpenFOAM not found**: Ensure environment is sourced with `source /opt/openfoam10/etc/bashrc`

**Python visualization issues**: Install required packages with `pip install pyvista numpy matplotlib`

**Mesh generation fails**: Check available memory (snappyHexMesh requires significant RAM)

**No VTK files**: Ensure `foamToVTK` completed successfully in the simulation

## 📚 Additional Resources

- [OpenFOAM Documentation](https://www.openfoam.com/documentation/)
- [PyVista Documentation](https://docs.pyvista.org/)
- [Azure Virtual Machines](https://azure.microsoft.com/en-us/services/virtual-machines/)

## 📄 License

See `LICENSE` file for details.
