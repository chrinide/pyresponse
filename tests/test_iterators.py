import numpy as np
import scipy as sp

import pyscf

from pyresponse import iterators, utils, magnetic
from . import molecules_pyscf as molecules


def test_iterators():

    mol = molecules.molecule_glycine_sto3g()
    mol.charge = 1
    mol.spin = 1
    mol.build()

    mf = pyscf.scf.uhf.UHF(mol)
    mf.scf()

    C = utils.fix_mocoeffs_shape(mf.mo_coeff)
    E = utils.fix_moenergies_shape(mf.mo_energy)
    occupations = utils.occupations_from_pyscf_mol(mol, C)

    solver_ref = iterators.ExactInv(C, E, occupations)
    calculator_ref = magnetic.Magnetizability(mol, C, E, occupations, solver=solver_ref)
    calculator_ref.form_operators()
    calculator_ref.run(hamiltonian='rpa', spin='singlet')
    calculator_ref.form_results()
    print(calculator_ref.magnetizability)

    ref = calculator_ref.magnetizability
    inv_funcs = (
        sp.linalg.inv,
        sp.linalg.pinv,
        sp.linalg.pinv2,
    )

    thresh = 6.0e-14

    for inv_func in inv_funcs:
        solver_res = iterators.ExactInv(C, E, occupations, inv_func=inv_func)
        calculator_res = magnetic.Magnetizability(mol, C, E, occupations, solver=solver_res)
        calculator_res.form_operators()
        calculator_res.run(hamiltonian='rpa', spin='singlet')
        calculator_res.form_results()
        print(calculator_res.magnetizability)

        assert np.all(np.equal(np.sign(calculator_ref.magnetizability),
                               np.sign(calculator_res.magnetizability)))
        diff = calculator_ref.magnetizability - calculator_res.magnetizability
        abs_diff = np.abs(diff)
        print(abs_diff)
        assert np.all(abs_diff < thresh)

    return


if __name__ == '__main__':
    test_iterators()
