import numpy as np
from Q import Q

def intgr(r, fi, psi, h, Wt, t):
    """
    Compute vertical and radial displacements Uz(r) and Ur(r).

    Parameters:
        r: numpy.ndarray
            Array of radial positions.
        fi: numpy.ndarray
            Basis function values fi.
        psi: numpy.ndarray
            Basis function values psi.
        h: float
            Parameter h used in calculations.
        Wt: numpy.ndarray
            Weight array for integration.
        t: numpy.ndarray
            Interval of integration.

    Returns:
        Uz: numpy.ndarray
            Vertical displacements.
        Ur: numpy.ndarray
            Radial displacements.
    """
    if r.ndim == 1:
        r = r.reshape(1, -1)
    s1, s2 = r.shape
    Uz = np.zeros_like(r)
    Ur = np.zeros_like(r)

    for i in range(s1):
        for j in range(s2):
            Uz[i, j] = np.sum(Wt * (fi * (Q(h, t, r[i, j], 1) + h * Q(h, t, r[i, j], 2)) +
                                    psi * (Q(h, t, r[i, j], 1) / t - Q(h, t, r[i, j], 3))))

            Ur[i, j] = np.sum(Wt * (psi * ((Q(h, t, r[i, j], 4) - h * Q(h, t, r[i, j], 5)) / t -
                                           Q(h, t, r[i, j], 6) + h * Q(h, t, r[i, j], 7)) -
                                     h * fi * Q(h, t, r[i, j], 8)))

    return Uz, Ur
