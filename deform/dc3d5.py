import numpy as np

def dc3d5(alpha, x, y, dip, al1, al2, aw1, aw2, disl1, disl2, disl3):
    """
    Compute displacements (ux, uy, uz) for a buried fault in a semi-infinite medium, including tensile components.

    Parameters:
        alpha: float
            Medium parameter.
        x: numpy.ndarray
            x-coordinates of observation points.
        y: numpy.ndarray
            y-coordinates of observation points.
        dip: float
            Dip angle of the fault (degrees).
        al1, al2: float
            Fault length parameters.
        aw1, aw2: float
            Fault width parameters.
        disl1, disl2, disl3: float
            Dislocation components.

    Returns:
        ux, uy, uz: numpy.ndarray
            Displacement components in x, y, and z directions.
        err: int
            Error flag (0 if no errors).
    """
    F0 = 0.0
    F1 = 1.0
    F2 = 2.0
    PI2 = 2 * np.pi
    EPS = 1.0e-6

    nx = len(x)

    u = np.zeros((3, nx))
    dub = np.zeros((3, nx))

    # Medium and fault dip constants
    c0_alp3 = (F1 - alpha) / alpha

    pl8 = PI2 / 360
    c0_sd = np.sin(dip * pl8)
    c0_cd = np.cos(dip * pl8)

    if abs(c0_cd) < EPS:
        c0_cd = F0
        c0_sd = F1 if c0_sd > F0 else -F1

    c0_cdcd = c0_cd**2
    c0_sdcd = c0_sd * c0_cd
    c0_sdsd = c0_sd**2

    # Geometric parameters
    p = y * c0_cd
    q = y * c0_sd

    jxi = ((x - al1) * (x - al2) <= F0)
    jet = ((p - aw1) * (p - aw2) <= F0)

    for k in range(2):
        et = p - aw1 if k == 0 else p - aw2
        for j in range(2):
            xi = x - al1 if j == 0 else x - al2

            # Station geometry constants with singularity handling
            etq_max = np.maximum(np.abs(et), np.abs(q))
            dc_max = np.maximum(np.abs(xi), etq_max)

            xi = xi - (np.abs(xi / dc_max) < EPS) * xi
            xi = xi - (np.abs(xi) < EPS) * xi
            et = et - (np.abs(et / dc_max) < EPS) * et
            et = et - (np.abs(et) < EPS) * et
            q = q - (np.abs(q / dc_max) < EPS) * q
            q = q - (np.abs(q) < EPS) * q

            dc_xi = xi
            dc_et = et
            dc_q = q

            c2_r = np.sqrt(dc_xi**2 + dc_et**2 + dc_q**2)

            if np.any(c2_r == F0):
                return np.zeros(nx), np.zeros(nx), np.zeros(nx), 1

            c2_y = dc_et * c0_cd + dc_q * c0_sd
            c2_d = dc_et * c0_sd - dc_q * c0_cd

            with np.errstate(divide='ignore', invalid='ignore'):
                c2_tt = np.arctan((dc_xi * dc_et) / (dc_q * c2_r))
            c2_tt = np.where(dc_q == 0, F0, c2_tt)

            c2_x11 = F1 / (c2_r * (c2_r + dc_xi))
            c2_x11 = c2_x11 - ((dc_xi < F0) & (dc_q == F0) & (dc_et == F0)) * c2_x11

            c2_ale_msk1 = ((dc_et < F0) & (dc_q == F0) & (dc_xi == F0)).astype(float)
            c2_ale_msk2 = F1 - c2_ale_msk1
            ret1 = c2_r - dc_et
            ret2 = c2_r + dc_et
            c2_ale = c2_ale_msk1 * (-np.log(ret1)) + c2_ale_msk2 * np.log(ret2)
            c2_y11 = F1 / (c2_r * ret2)

            if np.any(((q == F0) & (((jxi & (et == F0)) | (jet & (xi == F0)))) ) | (c2_r == F0)):
                return np.zeros(nx), np.zeros(nx), np.zeros(nx), 2

            rd = c2_r + c2_d
            if c0_cd != F0:
                xx = np.sqrt(xi**2 + q**2)
                ai4 = (xi != 0) * ((F1 / c0_cdcd) * (xi / rd * c0_sdcd +
                                  F2 * np.arctan((et * (xx + q * c0_cd) +
                                                  xx * (c2_r + xx) * c0_sd) /
                                                 (xi * (c2_r + xx) * c0_cd))))
                ai3 = (c2_y * c0_cd / rd - c2_ale + c0_sd * np.log(rd)) / c0_cdcd
            else:
                rd2 = rd**2
                ai3 = (et / rd + c2_y * q / rd2 - c2_ale) / F2
                ai4 = (xi * c2_y / rd2) / F2

            ai1 = -xi / rd * c0_cd - ai4 * c0_sd
            ai2 = np.log(rd) + ai3 * c0_sd

            qx = q * c2_x11
            qy = q * c2_y11

            # Strike-slip contribution
            if disl1 != F0:
                du2 = np.zeros((3, nx))
                du2[0, :] = -xi * qy - c2_tt - c0_alp3 * ai1 * c0_sd
                du2[1, :] = -q / c2_r + c0_alp3 * c2_y / rd * c0_sd
                du2[2, :] = q * qy - c0_alp3 * ai2 * c0_sd
                dub = (disl1 / PI2) * du2
            else:
                dub = np.zeros((3, nx))

            # Dip-slip contribution
            if disl2 != F0:
                du2 = np.zeros((3, nx))
                du2[0, :] = -q / c2_r + c0_alp3 * ai3 * c0_sdcd
                du2[1, :] = -et * qx - c2_tt - c0_alp3 * xi / rd * c0_sdcd
                du2[2, :] = q * qx + c0_alp3 * ai4 * c0_sdcd
                dub = dub + (disl2 / PI2) * du2

            # Tensile contribution
            if disl3 != F0:
                du2 = np.zeros((3, nx))
                du2[0, :] = q * qy - c0_alp3 * ai3 * c0_sdsd
                du2[1, :] = q * qx + c0_alp3 * xi / rd * c0_sdsd
                du2[2, :] = et * qx + xi * qy - c0_alp3 * ai4 * c0_sdsd - c2_tt
                dub = dub + (disl3 / PI2) * du2

            du = np.zeros((3, nx))
            du[0, :] = dub[0, :]
            du[1, :] = dub[1, :] * c0_cd - dub[2, :] * c0_sd
            du[2, :] = dub[1, :] * c0_sd + dub[2, :] * c0_cd

            if j == k:
                u += du
            else:
                u -= du

    return u[0, :], u[1, :], u[2, :], 0