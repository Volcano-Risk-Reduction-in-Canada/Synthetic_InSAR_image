import numpy as np
from dc3d4 import dc3d4
from dc3d5 import dc3d5
from dc3d6 import dc3d6

def disloc3d4(m, x, lambda_, mu):
    """
    Returns the deformation at points 'x', given dislocation model 'm'.

    Parameters:
        m: numpy.ndarray
            Dislocation model matrix (9xj).
        x: numpy.ndarray
            Observation coordinates matrix (2xi).
        lambda_: float
            First Lame parameter.
        mu: float
            Second Lame parameter (shear modulus).

    Returns:
        U: numpy.ndarray
            Displacements (east, north, and up components).
        flag: int
            Error flag (0 if no error).
    """
    DEG2RAD = 2 * np.pi / 360
    nfaults = m.shape[1]
    nx = x.shape[1]

    # Initialize displacement matrix
    U = np.zeros((3, nx))

    # Calculate alpha
    alpha = (lambda_ + mu) / (lambda_ + 2 * mu)
    # print(f"Alpha: {alpha}")

    # Loop over models
    for i in range(nfaults):
        flt_x = np.full(nx, m[0, i])
        flt_y = np.full(nx, m[1, i])
        strike = m[2, i]
        dip = m[3, i]
        rake = m[4, i]
        slip = m[5, i]
        length = m[6, i]
        hmin = m[7, i]
        hmax = m[8, i]

        if m[9, i] == 3:  # Sills
            dip = m[3, i]
            fdepth = hmin
            aw1 = -hmax / 2
            aw2 = hmax / 2
            w = hmax
        else:
            sindip = np.sin(dip * DEG2RAD)
            w = (hmax - hmin) / sindip
            aw1 = np.full(nx, hmin / sindip)
            aw2 = np.full(nx, hmax / sindip)

        rrake = (rake + 90) * DEG2RAD
        ud = np.full(nx, slip * np.cos(rrake))
        us = np.full(nx, -slip * np.sin(rrake))
        print(f'us: {us}')
        opening = np.full(nx, slip)
        halflen = length / 2
        al2 = np.full(nx, halflen)
        al1 = -al2

        if np.any(hmin < 0):
            raise ValueError("ERROR: Fault top above ground surface")
        
        hmin += (hmin == 0) * 1e-5  # Adjust if hmin is zero

        sstrike = (strike + 90) * DEG2RAD
        ct = np.cos(sstrike)
        st = np.sin(sstrike)

        X = ct * (-flt_x + x[0, :]) - st * (-flt_y + x[1, :])
        Y = ct * (-flt_y + x[1, :]) + st * (-flt_x + x[0, :])

        if m[9, i] == 1:  # Regular double couple fault
            ux, uy, uz, err = dc3d4(alpha, X, Y, -dip, al1, al2, aw1, aw2, us, ud)
        elif m[9, i] == 2:  # Tensile only component solution, dykes
            ux, uy, uz, err = dc3d5(alpha, X, Y, -dip, al1, al2, aw1, aw2, 0, 0, opening)
        elif m[9, i] == 3:  # Tensile only component solution, sills
            ux, uy, uz, err = dc3d6(alpha, X, Y, fdepth, -dip, al1, al2, aw1, aw2, 0, 0, opening)
        else:
            raise ValueError("10th row in geometry file must be 1 (=double couple) or 2 (tensile)")

        if err != 0:
            raise RuntimeError(f"Error code in dc3d3: {err}")

        U[0, :] += ct * ux + st * uy
        U[1, :] += -st * ux + ct * uy
        U[2, :] += uz

    return U, 0
