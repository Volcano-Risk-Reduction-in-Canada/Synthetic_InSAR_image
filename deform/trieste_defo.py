import numpy as np
import matplotlib.pyplot as plt
from phase_colormap import phase_colormap
from generateDeformation import generateDeformation

# Script to produce simulated interferograms
# Define Source Type
# 1 = Rectangular Dislocation (no opening) - Earthquake
# 2 = Rectangular Dislocation (opening only) - Dyke
# 3 = Rectangular Dislocation (opening only) - Sill
# 4 = Point Pressure Source (Mogi) - Magma Chamber
# 5 = Pressurized Penny-shaped Horizontal Crack (Fialko) - Sill

Source_Type = 2

# Define Source Parameters
Quake = {
    "Strike": 25,                # strike in degrees [0-180]
    "Dip": 80,                   # dip in degrees (usually 90 or near 90)
    "Rake": -90,                 # 
    "Slip": 1,
    "Top_depth": 1,
    "Bottom_depth": 10,
    "Length": 10
}

Dyke = {
    "Strike": 0,             # strike in degrees [0-180]
    "Dip": -90,                # dip in degrees (usually 90 or near 90)
    "Opening": 0.5,            # magnitude of opening (perpendincular to plane) in metres
    "Top_depth": 2,             # depth (measured vertically) to top of dyke in kilometres
    "Bottom_depth": 5,          # depth (measured vertically) to bottom of dyke in kilometres
    "Length": 8                 # dyke length in kilometres
}

Sill = {
    "Strike": 0, "Dip": 0, "Opening": 1.4,
    "Depth": 4.5, "Width": 1.4, "Length": 6.046
}

Mogi = {
    "Depth": 2.8, "Volume": 10**6.5
}

Penny = {
    "Depth": 5, "Pressure": 10**6, "Radius": 5
}

# Satellite parameters
values = np.arange(0, 61, 60)
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
    plt.imshow(los_grid_wrap / 0.028333 * 2 * np.pi - np.pi, extent=[x[0] / 1000, x[-1] / 1000, y[0] / 1000, y[-1] / 1000], cmap=phase_colormap())
    plt.colorbar(label='radians')
    plt.title(f'Wrapped Simulation (Heading: {Heading})')
    plt.xlabel('Easting (km)')
    plt.ylabel('Northing (km)')
    plt.axis('image')
    plt.show()
