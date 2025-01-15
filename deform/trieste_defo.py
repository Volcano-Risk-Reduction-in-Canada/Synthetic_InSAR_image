import numpy as np
import matplotlib.pyplot as plt
from generateDeformation import generateDeformation

# Script to produce simulated interferograms
# Define Source Type
# 1 = Rectangular Dislocation (no opening) - Earthquake
# 2 = Rectangular Dislocation (opening only) - Dyke
# 3 = Rectangular Dislocation (opening only) - Sill
# 4 = Point Pressure Source (Mogi) - Magma Chamber
# 5 = Pressurized Penny-shaped Horizontal Crack (Fialko) - Sill

Source_Type = 4

# Define Source Parameters
Quake = {
    "Strike": 25, "Dip": 80, "Rake": -90, "Slip": 1,
    "Top_depth": 1, "Bottom_depth": 10, "Length": 10
}

Dyke = {
    "Strike": 0, "Dip": 90, "Opening": 0.5,
    "Top_depth": 2, "Bottom_depth": 5, "Length": 8
}

Sill = {
    "Strike": 0, "Dip": 10, "Opening": 10,
    "Depth": 5, "Width": 0.5, "Length": 1
}

Mogi = {
    "Depth": 2.8, "Volume": 10**6.5
}

Penny = {
    "Depth": 5, "Pressure": 10**6, "Radius": 5
}

# Satellite parameters
values = np.arange(0, 360, 60)
Incidence = 5  # Incidence angle of satellite in degrees

# Grid parameters
x = np.arange(-25000, 25001, 100)  # Easting
y = np.arange(-25000, 25001, 100)  # Northing

for Heading in values:
    # Generate deformation based on Source_Type
    los_grid_wrap, los_grid = generateDeformation(
        Source_Type, x, y, Quake, Dyke, Sill, Mogi, Penny, Heading, Incidence
    )

    deformation_range = np.ptp(los_grid / 0.028333 * 2 * np.pi)
    print(f"Heading: {Heading}, Deformation Range: {deformation_range}")

    # Plot interferograms
    plt.figure()
    plt.imshow(los_grid_wrap / 0.028333 * 2 * np.pi - np.pi, extent=[x[0] / 1000, x[-1] / 1000, y[0] / 1000, y[-1] / 1000], cmap='jet')
    plt.colorbar(label='radians')
    plt.title(f'Wrapped Simulation (Heading: {Heading})')
    plt.xlabel('Easting (km)')
    plt.ylabel('Northing (km)')
    plt.axis('image')
    plt.show()
