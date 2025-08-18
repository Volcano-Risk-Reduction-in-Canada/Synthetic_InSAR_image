import numpy as np
from .Q import Q

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
    r = np.asarray(r)
    original_shape = r.shape
    if r.ndim == 1:
        r = r[np.newaxis, :]
    s1, s2 = r.shape
    Uz = np.zeros((s1, s2))
    Ur = np.zeros((s1, s2))

    for i in range(s1):
        for j in range(s2):
            rr = r[i, j]
            Uz[i, j] = np.sum(Wt * (fi * (Q(h, t, rr, 1) + h * Q(h, t, rr, 2)) +
                                    psi * (Q(h, t, rr, 1) / t - Q(h, t, rr, 3))))

            Ur[i, j] = np.sum(Wt * (psi * ((Q(h, t, rr, 4) - h * Q(h, t, rr, 5)) / t -
                                           Q(h, t, rr, 6) + h * Q(h, t, rr, 7)) -
                                     h * fi * Q(h, t, rr, 8)))

    return Uz.reshape(original_shape), Ur.reshape(original_shape)
