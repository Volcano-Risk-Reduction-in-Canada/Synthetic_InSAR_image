import numpy as np


def fpkernel(h, t, r, n):
    """Kernels calculation.

    Parameters
    ----------
    h : float
        Parameter h used in calculations.
    t : float
        Scalar t value.
    r : array_like
        Array of r values.
    n : int
        Kernel type (1, 2, 3, or 4).

    Returns
    -------
    numpy.ndarray
        Calculated kernel values.
    """
    r = np.asarray(r, dtype=float)
    t = float(np.asarray(t, dtype=float))
    p = 4 * h ** 2

    if n == 1:  # KN
        K = p * h * (KG(t - r, p) - KG(t + r, p))

    elif n == 2:  # KN1
        Dlt = 1e-6
        a = t + r
        b = t - r
        y = a ** 2
        z = b ** 2
        g = 2 * p * h * (p ** 2 + 6 * p * (t ** 2 + r ** 2) + 5 * (a * b) ** 2)
        s = ((p + z) * (p + y)) ** 2
        s = g / s
        trbl = -4 * h / (p + t ** 2) * np.ones_like(r)
        rs = r > Dlt
        if t < Dlt:
            trbl = -4 * h / (p + r ** 2)
        else:
            trbl[rs] = h / t / r[rs] * np.log((p + z[rs]) / (p + y[rs]))
        K = trbl + s + h * (KERN(b, p) + KERN(a, p))

    elif n == 3:  # KM
        y = (t + r) ** 2
        z = (t - r) ** 2
        a = ((p + y) * (p + z)) ** 2
        c = t + r
        d = t - r
        b = p * t * ((3 * p ** 2 - (c * d) ** 2 + 2 * p * (t ** 2 + r ** 2)) / a)
        a = p / 2 * (c * KG(c, p) + d * KG(d, p))
        K = b - a

    elif n == 4:  # KM1(t,r) = KM(r,t)
        y = (t + r) ** 2
        z = (t - r) ** 2
        a = ((p + y) * (p + z)) ** 2
        c = t + r
        d = -t + r
        b = p * r * ((3 * p ** 2 - (c * d) ** 2 + 2 * p * (t ** 2 + r ** 2)) / a)
        a = p / 2 * (c * KG(c, p) + d * KG(d, p))
        K = b - a

    else:
        raise ValueError("Invalid value for n. Must be 1, 2, 3, or 4.")

    return K


def KG(s, p):
    z = s ** 2
    y = p + z
    return (3 * p - z) / y ** 3


def KERN(w, p):
    u = (p + w ** 2) ** 3
    return 2 * (p ** 2 / 2 + w ** 4 - p * w ** 2 / 2) / u
