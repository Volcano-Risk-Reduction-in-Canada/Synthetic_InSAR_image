import numpy as np
from fredholm import fredholm
from intgr import intgr

def penny(mod, coord, mu, v):
    """
    Create displacement field for a penny-shaped crack model (Fialko et al., 2001).

    Parameters:
        mod: list
            [x_c, y_c, z_c, R, P], where
            x_c, y_c, z_c: Coordinates of the center of the crack (meters).
            R: Crack radius (meters).
            P: Pressure in the crack (Pa).
        coord: numpy.ndarray
            Observation coordinates (x, y) in meters.
        mu: float
            Shear modulus (Pa).
        v: float
            Poisson's ratio.

    Returns:
        Ux, Uy, Uz: numpy.ndarray
            Displacement components in the x, y, and z directions.
    """
    R = mod[3]
    P = mod[4]
    x = coord[:, 0] / R
    y = coord[:, 1] / R
    x_c = mod[0] / R
    y_c = mod[1] / R
    z_c = mod[2]

    # Convert pressure into non-dimensional factor
    Pf = 2 * (1 - v) * R * P / mu

    h = z_c / R  # Dimensionless crack depth

    # Integration parameters
    nis = 2  # Number of sub-intervals for Gauss quadrature
    eps = 1e-5  # Solution accuracy for Fredholm integral equations

    # Solve Fredholm integral equations
    fi, psi, t, Wt = fredholm(h, nis, eps)

    r = np.sqrt((x - x_c)**2 + (y - y_c)**2)
    Uz, Ur = intgr(r, fi, psi, h, Wt, t)

    Uz = -Uz * Pf
    Ur = Ur * Pf

    Nx = (x - x_c) / r  # Unit vector from crack center to observation point
    Ny = (y - y_c) / r

    Ux = Ur * Nx
    Uy = Ur * Ny

    return Ux, Uy, Uz
