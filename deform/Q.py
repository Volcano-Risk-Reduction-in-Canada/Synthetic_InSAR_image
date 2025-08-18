import numpy as np


def Q(h, t, r, n):
    """
    Kernels calculation.

    Parameters:
        h: float
            Parameter h.
        t: numpy.ndarray
            Interval of integration.
        r: numpy.ndarray or float
            Radial distance or scalar value.
        n: int
            Kernel type (1 to 8, 41, 51, 61).

    Returns:
        numpy.ndarray
            Calculated kernel values.
    """
    t = np.asarray(t, dtype=float)
    r = np.asarray(r, dtype=float)

    E = h**2 + r**2 - t**2
    D = np.sqrt(E**2 + 4 * h**2 * t**2)
    D3 = D**3

    if n == 1:  # Q1
        K = np.sqrt(2) * h * t / (D * np.sqrt(D + E))
    elif n == 2:  # Q2
        K = (1 / np.sqrt(2)) / D3 * (
            h * np.sqrt(D - E) * (2 * E + D) - t * np.sqrt(D + E) * (2 * E - D)
        )
    elif n == 3:  # Q3
        K = (1 / np.sqrt(2)) / D3 * (
            h * np.sqrt(D + E) * (2 * E - D) + t * np.sqrt(D - E) * (2 * E + D)
        )
    elif n == 4:  # Q4
        K = t / r - np.sqrt(D - E) / (r * np.sqrt(2))
    elif n == 5:  # Q5
        K = -(h * np.sqrt(D - E) - t * np.sqrt(D + E)) / (D * r * np.sqrt(2))
    elif n == 6:  # Q6
        K = 1 / r - (h * np.sqrt(D + E) + t * np.sqrt(D - E)) / (D * r * np.sqrt(2))
    elif n == 7:  # Q7
        K = r * np.sqrt(D + E) * (2 * E - D) / (D3 * np.sqrt(2))
    elif n == 8:  # Q8
        K = r * np.sqrt(D - E) * (2 * E + D) / (D3 * np.sqrt(2))
    elif n == 41:  # Q4*r
        K = t - np.sqrt(D - E) / np.sqrt(2)
    elif n == 51:  # Q5*r
        K = -(h * np.sqrt(D - E) - t * np.sqrt(D + E)) / (D * np.sqrt(2))
    elif n == 61:  # Q6*r
        K = 1 - (h * np.sqrt(D + E) + t * np.sqrt(D - E)) / (D * np.sqrt(2))
    else:
        K = np.array([])

    return K
