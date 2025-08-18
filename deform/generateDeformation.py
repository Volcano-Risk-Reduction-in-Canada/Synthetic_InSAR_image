import numpy as np
from .disloc3d4 import disloc3d4
from .rngchn_mogi import rngchn_mogi

def generateDeformation(Source_Type, x, y, Quake, Dyke, Sill, Mogi, Penny, Heading, Incidence):
    """
    Generate deformation based on the specified source type and parameters.

    Parameters:
        Source_Type: int
            Type of the source (1 to 5).
        x: numpy.ndarray
            Array of x-coordinates.
        y: numpy.ndarray
            Array of y-coordinates.
        Quake, Dyke, Sill, Mogi, Penny: dict
            Dictionaries containing parameters for the respective source types.
        Heading: float
            Heading angle in degrees.
        Incidence: float
            Incidence angle in degrees.

    Returns:
        los_grid_wrap: numpy.ndarray
            Wrapped line-of-sight deformation grid.
        los_grid: numpy.ndarray
            Unwrapped line-of-sight deformation grid.
    """
    # Define elastic Lame parameters
    lambda_ = 2.3e10  # Pascals
    mu = 2.3e10
    v = lambda_ / (2 * (lambda_ + mu))

    # Calculate LOS vector
    DEG2RAD = np.pi / 180
    sat_inc = 90 - Incidence
    sat_az = 360 - Heading
    los_x = -np.cos(sat_az * DEG2RAD) * np.cos(sat_inc * DEG2RAD)
    los_y = -np.sin(sat_az * DEG2RAD) * np.cos(sat_inc * DEG2RAD)
    los_z = np.sin(sat_inc * DEG2RAD)
    LOS_vector = np.array([los_x, los_y, los_z])

    # Set up model parameter vector and calculate coordinates for plotting
    if Source_Type == 1:
        model = np.array([1, 1, Quake['Strike'], Quake['Dip'], Quake['Rake'], Quake['Slip'],
                 Quake['Length'] * 1000, Quake['Top_depth'] * 1000, Quake['Bottom_depth'] * 1000, 1]).reshape(-1, 1)
    elif Source_Type == 2:
        model = np.array([1, 1, Dyke['Strike'], Dyke['Dip'], 0, Dyke['Opening'],
                 Dyke['Length'] * 1000, Dyke['Top_depth'] * 1000, Dyke['Bottom_depth'] * 1000, 2]).reshape(-1, 1)
    elif Source_Type == 3:
        model = np.array([1, 1, Sill['Strike'], Sill['Dip'], 0, Sill['Opening'],
                 Sill['Length'] * 1000, Sill['Depth'] * 1000, Sill['Width'] * 1000, 3]).reshape(-1, 1)
    elif Source_Type in [4, 5]:
        model = np.array([]).reshape(-1, 1)
    else:
        raise ValueError("Error: Source_Type must be 1, 2, 3, 4, or 5")

    # Calculate fault extents for visualization
    if Source_Type in [1, 2]:
        end1x = model[0, 0] + np.sin(model[2, 0] * DEG2RAD) * model[6, 0] / 2
        end2x = model[0, 0] - np.sin(model[2, 0] * DEG2RAD) * model[6, 0] / 2
        end1y = model[1, 0] + np.cos(model[2, 0] * DEG2RAD) * model[6, 0] / 2
        end2y = model[1, 0] - np.cos(model[2, 0] * DEG2RAD) * model[6, 0] / 2
        c1x = end1x + np.sin((model[2, 0] + 90) * DEG2RAD) * np.cos(model[3, 0] * DEG2RAD) * model[7, 0]
        c2x = end1x + np.sin((model[2, 0] + 90) * DEG2RAD) * np.cos(model[3, 0] * DEG2RAD) * model[8, 0]
        c3x = end2x + np.sin((model[2, 0] + 90) * DEG2RAD) * np.cos(model[3, 0] * DEG2RAD) * model[8, 0]
        c4x = end2x + np.sin((model[2, 0] + 90) * DEG2RAD) * np.cos(model[3, 0] * DEG2RAD) * model[7, 0]
        c1y = end1y + np.cos((model[2, 0] + 90) * DEG2RAD) * np.cos(model[3, 0] * DEG2RAD) * model[7, 0]
        c2y = end1y + np.cos((model[2, 0] + 90) * DEG2RAD) * np.cos(model[3, 0] * DEG2RAD) * model[8, 0]
        c3y = end2y + np.cos((model[2, 0] + 90) * DEG2RAD) * np.cos(model[3, 0] * DEG2RAD) * model[8, 0]
        c4y = end2y + np.cos((model[2, 0] + 90) * DEG2RAD) * np.cos(model[3, 0] * DEG2RAD) * model[7, 0]
    elif Source_Type == 3:
        end1x = model[0, 0] + np.sin(model[2, 0] * DEG2RAD) * model[6, 0] / 2
        end2x = model[0, 0] - np.sin(model[2, 0] * DEG2RAD) * model[6, 0] / 2
        end1y = model[1, 0] + np.cos(model[2, 0] * DEG2RAD) * model[6, 0] / 2
        end2y = model[1, 0] - np.cos(model[2, 0] * DEG2RAD) * model[6, 0] / 2
        width = model[8, 0] / 2
        c1x = end1x + np.sin((model[2, 0] + 90) * DEG2RAD) * np.cos(model[3, 0] * DEG2RAD) * width
        c2x = end1x - np.sin((model[2, 0] + 90) * DEG2RAD) * np.cos(model[3, 0] * DEG2RAD) * width
        c3x = end2x - np.sin((model[2, 0] + 90) * DEG2RAD) * np.cos(model[3, 0] * DEG2RAD) * width
        c4x = end2x + np.sin((model[2, 0] + 90) * DEG2RAD) * np.cos(model[3, 0] * DEG2RAD) * width
        c1y = end1y + np.cos((model[2, 0] + 90) * DEG2RAD) * np.cos(model[3, 0] * DEG2RAD) * width
        c2y = end1y - np.cos((model[2, 0] + 90) * DEG2RAD) * np.cos(model[3, 0] * DEG2RAD) * width
        c3y = end2y - np.cos((model[2, 0] + 90) * DEG2RAD) * np.cos(model[3, 0] * DEG2RAD) * width
        c4y = end2y + np.cos((model[2, 0] + 90) * DEG2RAD) * np.cos(model[3, 0] * DEG2RAD) * width

    # Set up regular grid for plots
    xx, yy = np.meshgrid(x, y)
    xx = xx.ravel()
    yy = yy.ravel()
    coords = np.vstack((xx, yy))

    # Calculate displacements
    if Source_Type in [1, 2, 3]:
        # print(f"Model: {model}")
        U, flag = disloc3d4(model, coords, lambda_, mu)
        xgrid = U[0, :].reshape(len(y), len(x))
        ygrid = U[1, :].reshape(len(y), len(x))
        zgrid = U[2, :].reshape(len(y), len(x))
        los_grid = xgrid * LOS_vector[0] + ygrid * LOS_vector[1] + zgrid * LOS_vector[2]
    elif Source_Type == 4:
        xgrid = rngchn_mogi(
            1 / 1000,
            1 / 1000,
            Mogi['Depth'],
            -Mogi['Volume'] / 1e9,
            coords[1, :] / 1000,
            coords[0, :] / 1000,
            v,
            np.tile([1.0, 0.0, 0.0], (coords.shape[1], 1)),
        )
        ygrid = rngchn_mogi(
            1 / 1000,
            1 / 1000,
            Mogi['Depth'],
            -Mogi['Volume'] / 1e9,
            coords[1, :] / 1000,
            coords[0, :] / 1000,
            v,
            np.tile([0.0, 1.0, 0.0], (coords.shape[1], 1)),
        )
        zgrid = rngchn_mogi(
            1 / 1000,
            1 / 1000,
            Mogi['Depth'],
            -Mogi['Volume'] / 1e9,
            coords[1, :] / 1000,
            coords[0, :] / 1000,
            v,
            np.tile([0.0, 0.0, 1.0], (coords.shape[1], 1)),
        )
        los_grid = rngchn_mogi(
            1 / 1000,
            1 / 1000,
            Mogi['Depth'],
            -Mogi['Volume'] / 1e9,
            coords[1, :] / 1000,
            coords[0, :] / 1000,
            v,
            np.tile(LOS_vector, (coords.shape[1], 1)),
        )
        xgrid = xgrid.reshape(len(y), len(x))
        ygrid = ygrid.reshape(len(y), len(x))
        zgrid = zgrid.reshape(len(y), len(x))
        los_grid = los_grid.reshape(len(y), len(x))
    elif Source_Type == 5:
        from .penny import penny
        model = [1, 1, Penny['Depth'] * 1000, Penny['Radius'] * 1000, Penny['Pressure']]
        xgrid, ygrid, zgrid = penny(model, coords.T, mu, v)
        los_grid = xgrid * LOS_vector[0] + ygrid * LOS_vector[1] + zgrid * LOS_vector[2]
        los_grid = los_grid.reshape(len(y), len(x))

    # Calculate wrapped interferogram
    los_grid_wrap = np.mod(los_grid + 10000, 0.028333)

    return los_grid_wrap, los_grid
