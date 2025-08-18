import numpy as np


def rngchn_mogi(n1, e1, depth, del_v, ning, eing, v, plook):
    """Range change from a Mogi source.

    Parameters
    ----------
    n1, e1 : float
        Local north and east coordinates of the source centre (km).
    depth : float
        Depth of the Mogi source (km).
    del_v : float
        Volume change of the source (km^3).
    ning, eing : array_like
        North and east coordinates at which to compute range change.  They may
        be vectors of equal length or a column/row vector pair for matrix
        output.
    v : float
        Poisson's ratio of the material.
    plook : array_like
        Look vector(s).  For vector geometry this should be an ``(N,3)`` array;
        for matrix geometry a length‑3 vector is expected.

    Returns
    -------
    numpy.ndarray
        Range change at the specified coordinates.
    """

    ning = np.asarray(ning)
    eing = np.asarray(eing)
    plook = np.asarray(plook)

    dsp_coef = 1_000_000 * del_v * (1 - v) / np.pi

    # Matrix output: ning is column vector, eing is row vector
    if (
        ning.ndim == 2
        and eing.ndim == 2
        and ning.shape[1] == 1
        and eing.shape[0] == 1
    ):
        print("Calculating a matrix of rngchg values")
        m = ning.shape[0]
        nn = eing.shape[1]
        tmp_n = np.tile(ning, (1, nn))
        tmp_e = np.tile(eing, (m, 1))

        d_mat = np.sqrt((tmp_n - n1) ** 2 + (tmp_e - e1) ** 2)
        tmp_hyp = (d_mat ** 2 + depth ** 2) ** 1.5
        del_d = dsp_coef * d_mat / tmp_hyp
        del_f = dsp_coef * depth / tmp_hyp
        azim = np.arctan2((tmp_e - e1), (tmp_n - n1))
        e_disp = np.sin(azim) * del_d
        n_disp = np.cos(azim) * del_d

        del_rng = np.empty_like(d_mat)
        for i in range(nn):
            del_rng[:, i] = np.dot(
                np.column_stack((e_disp[:, i], n_disp[:, i], del_f[:, i])), plook
            )

    # Vector output: ning and eing are co-linear vectors
    elif (
        (ning.ndim == 1 and eing.ndim == 1)
        or (ning.ndim == 2 and ning.shape[0] == 1 and eing.ndim == 2 and eing.shape[0] == 1)
        or (ning.ndim == 2 and ning.shape[1] == 1 and eing.ndim == 2 and eing.shape[1] == 1)
    ):
        ning_vec = ning.ravel()
        eing_vec = eing.ravel()
        if ning_vec.size != eing_vec.size:
            raise ValueError("Coord vectors not equal length!")

        d_mat = np.sqrt((ning_vec - n1) ** 2 + (eing_vec - e1) ** 2)
        tmp_hyp = (d_mat ** 2 + depth ** 2) ** 1.5
        del_d = dsp_coef * d_mat / tmp_hyp
        del_f = dsp_coef * depth / tmp_hyp
        azim = np.arctan2((eing_vec - e1), (ning_vec - n1))
        e_disp = np.sin(azim) * del_d
        n_disp = np.cos(azim) * del_d

        del_rng = (
            np.column_stack((e_disp, n_disp, del_f)) * plook
        ).sum(axis=1)
        del_rng = -1.0 * del_rng / 1000.0
        del_rng = del_rng.reshape(ning.shape)

    else:
        raise ValueError("Coord vectors make no sense!")

    return del_rng
