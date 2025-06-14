#!/usr/bin/env python3
"""
Streamlined motorbike mesh visualization for OpenFOAM results.
Provides simple, detailed, and exploded view options.
"""

import os
import pyvista as pv
import numpy as np

def load_motorbike_parts():
    """Load all motorbike mesh parts from VTK files"""
    bike_parts = []
    for root, dirs, files in os.walk("motorBike-VTK"):
        for fname in files:
            if fname.endswith("_500.vtk") and fname != "motorBike_500.vtk":
                part_path = os.path.join(root, fname)
                try:
                    bike_parts.append(pv.read(part_path))
                except:
                    continue
    return bike_parts

def simple_view():
    """Simple visualization with uniform coloring"""
    bike_parts = load_motorbike_parts()
    combined_bike = pv.MultiBlock(bike_parts).combine()
    
    plotter = pv.Plotter(title="Motorbike Mesh - Simple View")
    plotter.add_mesh(combined_bike, color="lightgray", opacity=0.7, show_edges=True, 
                    edge_color="black", line_width=0.5)
    
    plotter.set_background("white")
    plotter.add_axes(line_width=4)
    plotter.show_grid(color="lightgray")
    plotter.view_isometric()
    plotter.camera.azimuth = 45
    plotter.camera.elevation = 25
    plotter.camera.zoom(1.2)
    plotter.add_light(pv.Light(position=(10, 10, 10), intensity=0.8))
    plotter.add_light(pv.Light(position=(-5, 5, 5), intensity=0.4))
    
    plotter.show()

def detailed_view():
    """Detailed visualization with color-coded parts"""
    bike_parts = load_motorbike_parts()
    
    part_colors = {
        'frame': 'darkred', 'engine': 'darkgray', 'wheel': 'black', 'tyre': 'dimgray',
        'brake': 'silver', 'fairing': 'blue', 'fuel-tank': 'red', 'seat': 'brown',
        'rider': 'navy', 'exhaust': 'darkslategray', 'light': 'yellow', 'chain': 'gold'
    }
    
    def get_part_color(index):
        colors = list(part_colors.values())
        return colors[index % len(colors)]
    
    plotter = pv.Plotter(title="Motorbike Mesh - Detailed View")
    
    for i, part in enumerate(bike_parts):
        color = get_part_color(i)
        plotter.add_mesh(part, color=color, opacity=0.9, show_edges=True, 
                        edge_color='black', line_width=0.3)
    
    plotter.set_background("white")
    plotter.add_axes(line_width=4)
    plotter.show_grid(color="lightgray")
    plotter.view_isometric()
    plotter.camera.azimuth = 45
    plotter.camera.elevation = 25
    plotter.camera.zoom(1.2)
    plotter.add_light(pv.Light(position=(10, 10, 10), intensity=0.8))
    plotter.add_light(pv.Light(position=(-5, 5, 5), intensity=0.4))
    
    plotter.show()

def exploded_view():
    """Exploded view showing parts separated"""
    bike_parts = load_motorbike_parts()
    
    all_centers = [part.center for part in bike_parts]
    global_center = np.mean(all_centers, axis=0)
    explosion_factor = 0.3
    colors = ['red', 'blue', 'green', 'orange', 'purple', 'brown', 'pink', 'gray']
    
    plotter = pv.Plotter(title="Motorbike Mesh - Exploded View")
    
    for i, part in enumerate(bike_parts):
        offset_direction = np.array(part.center) - global_center
        if np.linalg.norm(offset_direction) > 0:
            offset_direction = offset_direction / np.linalg.norm(offset_direction)
        else:
            offset_direction = np.array([0, 0, 0])
        
        exploded_part = part.translate(offset_direction * explosion_factor)
        color = colors[i % len(colors)]
        plotter.add_mesh(exploded_part, color=color, opacity=0.8, show_edges=True, 
                        edge_color="black", line_width=0.2)
    
    plotter.set_background("lightgray")
    plotter.add_axes(line_width=4)
    plotter.view_isometric()
    plotter.camera.azimuth = 30
    plotter.camera.elevation = 20
    plotter.camera.zoom(0.7)
    
    plotter.show()

if __name__ == "__main__":
    print("Motorbike Mesh Visualization")
    print("1. Simple view")
    print("2. Detailed view")
    print("3. Exploded view")
    
    choice = input("Enter choice (1-3): ").strip()
    
    if choice == "1":
        simple_view()
    elif choice == "2":
        detailed_view()
    elif choice == "3":
        exploded_view()
    else:
        print("Invalid choice, showing simple view")
        simple_view()
