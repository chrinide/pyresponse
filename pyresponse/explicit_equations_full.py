import numpy as np

from .utils import form_vec_energy_differences


def form_rpa_a_matrix_mo_singlet_full(E_MO, TEI_MO, nocc):
    r"""Form the A (CIS) matrix for RPA in the molecular orbital (MO)
basis. [singlet]

    The equation for element :math:`\{ia,jb\}` is
    :math:`\left<aj||ib\right> = \left<aj|ib\right> -
    \left<aj|bi\right> = [ai|jb] - [ab|ji] = 2(ai|jb) - (ab|ji)`. It
    also includes the virt-occ energy difference on the diagonal.

    """

    norb = E_MO.shape[0]
    nvirt = norb - nocc
    nov = nocc * nvirt

    ediff = form_vec_energy_differences(np.diag(E_MO)[:nocc],
                                        np.diag(E_MO)[nocc:])

    A = np.empty(shape=(nov, nov))

    for i in range(nocc):
        for a in range(nvirt):
            ia = i*nvirt + a
            for j in range(nocc):
                for b in range(nvirt):
                    jb = j*nvirt + b
                    A[ia, jb] = 2*TEI_MO[a + nocc, i, j, b + nocc] - TEI_MO[a + nocc, b + nocc, j, i]

    A += np.diag(ediff)

    return A


def form_rpa_a_matrix_mo_triplet_full(E_MO, TEI_MO, nocc):
    """Form the A (CIS) matrix for RPA in the molecular orbital (MO)
    basis. [triplet]

    The equation for element {ia,jb} is - <aj|bi> = - [ab|ji] = -
    (ab|ji). It also includes the virt-occ energy difference on the
    diagonal.
    """

    norb = E_MO.shape[0]
    nvirt = norb - nocc
    nov = nocc * nvirt

    ediff = form_vec_energy_differences(np.diag(E_MO)[:nocc],
                                        np.diag(E_MO)[nocc:])

    A = np.empty(shape=(nov, nov))

    for i in range(nocc):
        for a in range(nvirt):
            ia = i*nvirt + a
            for j in range(nocc):
                for b in range(nvirt):
                    jb = j*nvirt + b
                    A[ia, jb] = - TEI_MO[a + nocc, b + nocc, j, i]

    A += np.diag(ediff)

    return A


def form_rpa_b_matrix_mo_singlet_full(TEI_MO, nocc):
    """Form the B matrix for RPA in the molecular orbital (MO)
    basis. [singlet]

    The equation for element {ia,jb} is <ab||ij> = <ab|ij> - <ab|ji> =
    [ai|bj] - [aj|bi] = 2*(ai|bj) - (aj|bi).
    """

    norb = TEI_MO.shape[0]
    nvirt = norb - nocc
    nov = nocc * nvirt

    B = np.empty(shape=(nov, nov))

    for i in range(nocc):
        for a in range(nvirt):
            ia = i*nvirt + a
            for j in range(nocc):
                for b in range(nvirt):
                    jb = j*nvirt + b
                    B[ia, jb] = 2*TEI_MO[a + nocc, i, b + nocc, j] - TEI_MO[a + nocc, j, b + nocc, i]

    return -B


def form_rpa_b_matrix_mo_triplet_full(TEI_MO, nocc):

    norb = TEI_MO.shape[0]
    nvirt = norb - nocc
    nov = nocc * nvirt

    B = np.empty(shape=(nov, nov))

    for i in range(nocc):
        for a in range(nvirt):
            ia = i*nvirt + a
            for j in range(nocc):
                for b in range(nvirt):
                    jb = j*nvirt + b
                    B[ia, jb] = - TEI_MO[a + nocc, j, b + nocc, i]

    return -B


def form_rpa_a_matrix_mo_singlet_ss_full(E_MO, TEI_MO, nocc):

    norb = E_MO.shape[0]
    nvirt = norb - nocc
    nov = nocc * nvirt

    ediff = form_vec_energy_differences(np.diag(E_MO)[:nocc],
                                        np.diag(E_MO)[nocc:])

    A = np.empty(shape=(nov, nov))

    for i in range(nocc):
        for a in range(nvirt):
            ia = i*nvirt + a
            for j in range(nocc):
                for b in range(nvirt):
                    jb = j*nvirt + b
                    A[ia, jb] = TEI_MO[a + nocc, i, j, b + nocc] - TEI_MO[a + nocc, b + nocc, j, i]

    A += np.diag(ediff)

    return A


def form_rpa_a_matrix_mo_singlet_os_full(TEI_MO_xxyy, nocc_x, nocc_y):

    nvirt_x = TEI_MO_xxyy.shape[0] - nocc_x
    nvirt_y = TEI_MO_xxyy.shape[2] - nocc_y
    nov_x = nocc_x * nvirt_x
    nov_y = nocc_y * nvirt_y

    A = np.empty(shape=(nov_x, nov_y))

    for i in range(nocc_x):
        for a in range(nvirt_x):
            ia = i*nvirt_x + a
            for j in range(nocc_y):
                for b in range(nvirt_y):
                    jb = j*nvirt_y + b
                    # TODO
                    A[ia, jb] = TEI_MO_xxyy[a + nocc_x, i, j, b + nocc_y]

    return A


def form_rpa_b_matrix_mo_singlet_ss_full(TEI_MO, nocc):

    norb = TEI_MO.shape[0]
    nvirt = norb - nocc
    nov = nocc * nvirt

    B = np.empty(shape=(nov, nov))

    for i in range(nocc):
        for a in range(nvirt):
            ia = i*nvirt + a
            for j in range(nocc):
                for b in range(nvirt):
                    jb = j*nvirt + b
                    B[ia, jb] = TEI_MO[a + nocc, i, b + nocc, j] - TEI_MO[a + nocc, j, b + nocc, i]

    return -B


def form_rpa_b_matrix_mo_singlet_os_full(TEI_MO_xxyy, nocc_x, nocc_y):

    nvirt_x = TEI_MO_xxyy.shape[0] - nocc_x
    nvirt_y = TEI_MO_xxyy.shape[2] - nocc_y
    nov_x = nocc_x * nvirt_x
    nov_y = nocc_y * nvirt_y

    B = np.empty(shape=(nov_x, nov_y))

    for i in range(nocc_x):
        for a in range(nvirt_x):
            ia = i*nvirt_x + a
            for j in range(nocc_y):
                for b in range(nvirt_y):
                    jb = j*nvirt_y + b
                    # TODO
                    B[ia, jb] = TEI_MO_xxyy[a + nocc_x, i, b + nocc_y, j]

    return -B
