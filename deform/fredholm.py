import numpy as np
from .fpkernel import fpkernel
from .RtWt import RtWt


def fredholm(h, m, er=1e-7):
    # Constants and initial setup
    lamda = 2 / np.pi

    Root, Weight = RtWt()

    NumLegendreTerms = len(Root)
    t = np.zeros(m * NumLegendreTerms)
    Wt = np.zeros_like(t)

    for k in range(1, m + 1):
        for i in range(1, NumLegendreTerms + 1):
            d1 = 1 / m
            t1 = d1 * (k - 1)
            r1 = d1 * k
            j = NumLegendreTerms * (k - 1) + i - 1
            t[j] = Root[i - 1] * (r1 - t1) * 0.5 + (r1 + t1) * 0.5
            Wt[j] = 0.5 / m * Weight[i - 1]

    fi1 = -lamda * t
    psi1 = np.zeros_like(t)
    fi = np.zeros_like(t)
    psi = np.zeros_like(t)

    res = 1e9

    while res > er:
        for i in range(m * NumLegendreTerms):
            fi[i] = -t[i] + np.sum(
                Wt * (fi1 * fpkernel(h, t[i], t, 1) + psi1 * fpkernel(h, t[i], t, 3))
            )
            psi[i] = np.sum(
                Wt * (psi1 * fpkernel(h, t[i], t, 2) + fi1 * fpkernel(h, t[i], t, 4))
            )

        fi *= lamda
        psi *= lamda

        # find maximum relative change
        diff_fi = np.abs(fi1 - fi)
        im = np.argmax(diff_fi)
        fim = diff_fi[im] / abs(fi[im])

        diff_psi = np.abs(psi1 - psi)
        im = np.argmax(diff_psi)
        psim = diff_psi[im] / abs(psi[im])

        res = max(fim, psim)

        fi1 = fi.copy()
        psi1 = psi.copy()

    return fi, psi, t, Wt
