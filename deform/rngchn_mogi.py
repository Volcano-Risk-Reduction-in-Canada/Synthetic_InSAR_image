import numpy as np

def rngchn_mogi(n1, e1, depth, del_v, ning, eing, v, plook):
    """
    Calculate range change based on the Mogi model.

    Parameters:
        n1: float
            Local north coordinate of the center of the Mogi source (km).
        e1: float
            Local east coordinate of the center of the Mogi source (km).
        depth: float
            Depth of the Mogi source (km).
        del_v: float
            Volume change of the Mogi source (km^3).
        ning: numpy.ndarray
            North coordinates of points to calculate range change.
        eing: numpy.ndarray
            East coordinates of points to calculate range change.
        v: float
            Poisson's ratio of the material.
        plook: numpy.ndarray
            Look vector array.

    Returns:
        numpy.ndarray
            Range change at coordinates given in ning and eing.
    """
    dsp_coef = 1e6 * del_v * (1 - v) / np.pi

    if ning.ndim == 2 and eing.ndim == 2:
        print("Calculating a matrix of range change values")
        m, nn = ning.shape
        del_rng = np.zeros_like(ning)
        tmp_n = np.zeros_like(ning)
        tmp_e = np.zeros_like(eing)

        for i in range(m):
            tmp_e[i, :] = eing[i, :]
        for j in range(nn):
            tmp_n[:, j] = ning[:, j]

        d_mat = np.sqrt((tmp_n - n1)**2 + (tmp_e - e1)**2)
        tmp_hyp = (d_mat**2 + depth**2)**1.5

        del_d = dsp_coef * d_mat / tmp_hyp
        del_f = dsp_coef * depth / tmp_hyp
        azim = np.arctan2((tmp_e - e1), (tmp_n - n1))

        e_disp = np.sin(azim) * del_d
        n_disp = np.cos(azim) * del_d

        for i in range(nn):
            del_rng[:, i] = np.dot(np.column_stack((e_disp[:, i], n_disp[:, i], del_f[:, i])), plook)

    elif ning.ndim == 1 and eing.ndim == 1:
        if ning.size != eing.size:
            raise ValueError("Coordinate vectors are not of equal length!")

        del_rng = np.zeros_like(ning)
        d_mat = np.sqrt((ning - n1)**2 + (eing - e1)**2)
        tmp_hyp = (d_mat**2 + depth**2)**1.5

        del_d = dsp_coef * d_mat / tmp_hyp
        del_f = dsp_coef * depth / tmp_hyp
        azim = np.arctan2((eing - e1), (ning - n1))

        e_disp = np.sin(azim) * del_d
        n_disp = np.cos(azim) * del_d

        del_rng = (np.column_stack((e_disp, n_disp, del_f)) * plook).sum(axis=1)
        del_rng = -1.0 * del_rng / 1000  # Convert from mm to m

    else:
        raise ValueError("Coordinate vectors make no sense!")

    return del_rng
