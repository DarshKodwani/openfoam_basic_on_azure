#!/bin/bash

set -e  # Exit if any command fails

echo "🔧 Setting up OpenFOAM motorBike tutorial..."

# Create a clean working directory
mkdir -p ~/openfoam-tests
cd ~/openfoam-tests

# Copy the motorBike tutorial
cp -r $FOAM_TUTORIALS/incompressible/simpleFoam/motorBike .

cd motorBike

# Make geometry folder if not already present
mkdir -p constant/geometry

# Copy and unzip the motorBike.obj.gz file
cp $FOAM_TUTORIALS/resources/geometry/motorBike.obj.gz constant/geometry/
gunzip -f constant/geometry/motorBike.obj.gz

echo "📦 Running blockMesh..."
blockMesh

echo "📐 Extracting surface features..."
surfaceFeatures

echo "🔲 Running snappyHexMesh..."
snappyHexMesh -overwrite

echo "  Running surfaceCheck (optional)..."
surfaceCheck constant/geometry/motorBike.obj || echo "(non-critical)"

echo "💨 Running simpleFoam simulation..."
simpleFoam

echo "📤 Converting results to VTK format..."
foamToVTK

echo "✅ Simulation complete. VTK results are in the 'VTK/' folder. Use ParaView or PyVista to view them."
