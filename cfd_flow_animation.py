#!/usr/bin/env python3
"""
Streamlined CFD animation generator for OpenFOAM motorbike simulation.
Creates a 2x2 grid showing velocity, pressure, geometry, and flow analysis.
"""

import os
import pyvista as pv
import numpy as np

def load_data():
    """Load volume data and motorbike parts"""
    volume_file = os.path.join("motorBike-VTK", "motorBike_500.vtk")
    volume_mesh = pv.read(volume_file)
    
    bike_parts = []
    for root, dirs, files in os.walk("motorBike-VTK"):
        for fname in files:
            if fname.endswith("_500.vtk") and fname != "motorBike_500.vtk":
                part_path = os.path.join(root, fname)
                try:
                    bike_parts.append(pv.read(part_path))
                except:
                    continue
    
    return volume_mesh, pv.MultiBlock(bike_parts).combine()

def setup_velocity_view(plotter, volume_mesh, bike_surface, angle):
    """Setup velocity field visualization"""
    plotter.subplot(0, 0)
    plotter.add_text("Velocity Field (m/s)", position='upper_left', font_size=12, color='black')
    
    center = volume_mesh.center
    slice_long = volume_mesh.slice(origin=center, normal=[0, 1, 0])
    slice_wake = volume_mesh.slice(origin=[center[0]+1.0, center[1], center[2]], normal=[1, 0, 0])
    slice_ground = volume_mesh.slice(origin=[center[0], center[1], 0.8], normal=[0, 0, 1])
    
    plotter.add_mesh(slice_long, scalars="U", cmap="jet", opacity=0.9, show_scalar_bar=False)
    plotter.add_mesh(slice_wake, scalars="U", cmap="coolwarm", opacity=0.6, show_scalar_bar=False)
    plotter.add_mesh(slice_ground, scalars="U", cmap="plasma", opacity=0.4, show_scalar_bar=False)
    plotter.add_mesh(bike_surface, color="silver", opacity=0.7, show_edges=True, edge_color="black", line_width=0.2)
    plotter.add_scalar_bar(title="Velocity", position_x=0.85, width=0.05, height=0.3, title_font_size=8, label_font_size=7)
    
    plotter.set_background("white")
    plotter.view_isometric()
    plotter.camera.azimuth = angle * 0.5
    plotter.camera.elevation = 20
    plotter.camera.zoom(1.2)

def setup_pressure_view(plotter, volume_mesh, bike_surface, angle):
    """Setup pressure field visualization"""
    plotter.subplot(0, 1)
    plotter.add_text("Pressure Field (Pa)", position='upper_left', font_size=12, color='black')
    
    center = volume_mesh.center
    slice_back = volume_mesh.slice(origin=[center[0] + 0.5, center[1], center[2]], normal=[1, 0, 0])
    slice_front = volume_mesh.slice(origin=[center[0] - 0.5, center[1], center[2]], normal=[1, 0, 0])
    
    plotter.add_mesh(slice_back, scalars="p", cmap="coolwarm", opacity=0.9, show_scalar_bar=False)
    plotter.add_mesh(slice_front, scalars="p", cmap="RdBu", opacity=0.6, show_scalar_bar=False)
    plotter.add_mesh(bike_surface, color="darkgray", opacity=0.5, show_edges=True, edge_color="black", line_width=0.3)
    plotter.add_scalar_bar(title="Pressure", position_x=0.85, width=0.05, height=0.3, title_font_size=8, label_font_size=7)
    
    plotter.set_background("white")
    plotter.view_isometric()
    plotter.camera.azimuth = angle * 0.5
    plotter.camera.elevation = 20
    plotter.camera.zoom(1.2)

def setup_mesh_view(plotter, bike_surface, angle):
    """Setup clean mesh visualization"""
    plotter.subplot(1, 0)
    plotter.add_text("Motorbike Geometry", position='upper_left', font_size=12, color='black')
    
    plotter.add_mesh(bike_surface, color="silver", opacity=0.9, show_edges=True, edge_color="black", line_width=0.4)
    
    plotter.set_background("white")
    plotter.view_isometric()
    plotter.camera.azimuth = angle
    plotter.camera.elevation = 25
    plotter.camera.zoom(1.3)

def setup_flow_analysis(plotter, volume_mesh, bike_surface, angle):
    """Setup flow analysis visualization"""
    plotter.subplot(1, 1)
    plotter.add_text("Flow Analysis & Wake", position='upper_left', font_size=12, color='black')
    
    center = volume_mesh.center
    wake_slice = volume_mesh.slice(origin=[center[0]+2.0, center[1], center[2]], normal=[1, 0, 0])
    
    if "omega" in volume_mesh.array_names:
        plotter.add_mesh(wake_slice, scalars="omega", cmap="turbo", opacity=0.8, show_scalar_bar=False)
        field_name = "Turbulence"
    elif "k" in volume_mesh.array_names:
        plotter.add_mesh(wake_slice, scalars="k", cmap="hot", opacity=0.8, show_scalar_bar=False)
        field_name = "Turbulent Energy"
    else:
        plotter.add_mesh(wake_slice, scalars="U", cmap="viridis", opacity=0.8, show_scalar_bar=False)
        field_name = "Velocity"
    
    try:
        seed_points = [[center[0]-3, y, z] for y in [-1.0, 0.0, 1.0] for z in [1.5, 2.0, 2.5]]
        seed_poly = pv.PolyData(seed_points)
        streamlines = volume_mesh.streamlines_from_source(seed_poly, vectors="U", max_steps=100, integration_direction='forward')
        plotter.add_mesh(streamlines, scalars="U", cmap="rainbow", line_width=2, opacity=0.9, show_scalar_bar=False)
    except:
        pass
    
    plotter.add_mesh(bike_surface, color="darkblue", opacity=0.6, show_edges=True, edge_color="navy", line_width=0.3)
    plotter.add_scalar_bar(title=field_name, position_x=0.85, width=0.05, height=0.3, title_font_size=8, label_font_size=7)
    
    plotter.set_background("lightgray")
    plotter.view_isometric()
    plotter.camera.azimuth = angle * 0.3
    plotter.camera.elevation = 15
    plotter.camera.zoom(1.0)

def create_animation():
    """Create the CFD animation"""
    output_file = "motorbike_cfd_analysis.mp4"
    fps, duration = 20, 10
    total_frames = fps * duration
    
    volume_mesh, bike_surface = load_data()
    plotter = pv.Plotter(shape=(2, 2), off_screen=True, window_size=(1920, 1080))
    angles = np.linspace(0, 360, total_frames, endpoint=False)
    
    plotter.open_movie(output_file, framerate=fps, quality=9)
    
    for i, angle in enumerate(angles):
        for row in range(2):
            for col in range(2):
                plotter.subplot(row, col)
                plotter.clear()
        
        setup_velocity_view(plotter, volume_mesh, bike_surface, angle)
        setup_pressure_view(plotter, volume_mesh, bike_surface, angle)
        setup_mesh_view(plotter, bike_surface, angle)
        setup_flow_analysis(plotter, volume_mesh, bike_surface, angle)
        
        plotter.write_frame()
        
        if (i + 1) % (total_frames // 10) == 0:
            print(f"Progress: {((i + 1) / total_frames) * 100:.0f}%")
    
    plotter.close()
    
    file_size = os.path.getsize(output_file) / (1024 * 1024)
    print(f"\n✅ Animation saved: {output_file}")
    print(f"📊 Size: {file_size:.1f} MB | Duration: {duration}s | FPS: {fps}")

if __name__ == "__main__":
    print("Creating CFD Animation...")
    create_animation()
    print("🎉 Complete!")
