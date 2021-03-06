import numpy as np
import scipy.constants as spc

from . import helpers
from .operators import Operator
from .molecular_property import ResponseProperty
from .utils import tensor_printer


class Magnetizability(ResponseProperty):

    def __init__(self, pyscfmol, mocoeffs, moenergies, occupations, use_giao=False, *args, **kwargs):
        super().__init__(pyscfmol, mocoeffs, moenergies, occupations, frequencies=[0.0], *args, **kwargs)
        self.use_giao = use_giao

    def form_operators(self):

        # angular momentum
        if self.use_giao:
            operator_angmom = Operator(label='angmom', is_imaginary=True, is_spin_dependent=False, triplet=False)
            integrals_angmom_ao = self.pyscfmol.intor('cint1e_giao_irjxp_sph', comp=3)
        else:
            operator_angmom = Operator(label='angmom', is_imaginary=True, is_spin_dependent=False, triplet=False)
            integrals_angmom_ao = self.pyscfmol.intor('cint1e_cg_irxp_sph', comp=3)
        operator_angmom.ao_integrals = integrals_angmom_ao
        self.driver.add_operator(operator_angmom)

    def form_results(self):

        assert len(self.driver.results) == 1
        operator_angmom = self.driver.solver.operators[0]
        self.magnetizability = (1 / 4) * self.driver.results[0]
        # print('paramagnetic part of magnetic susceptibility/magnetizability, no GIAO, Cartesian origin')
        # print(self.magnetizability)


class ElectronicGTensor(ResponseProperty):

    def __init__(self, pyscfmol, mocoeffs, moenergies, occupations, gauge_origin='ecc', *args, **kwargs):
        super().__init__(pyscfmol, mocoeffs, moenergies, occupations, frequencies=[0.0], *args, **kwargs)

        assert isinstance(gauge_origin, (str, list, tuple, np.ndarray))
        if isinstance(gauge_origin, str):
            coords = pyscfmol.atom_coords()
            charges = pyscfmol.atom_charges()
            is_uhf = mocoeffs.shape[0] == 2
            if is_uhf:
                Ca = mocoeffs[0, ...]
                Cb = mocoeffs[1, ...]
                nocc_a, _, nocc_b, _ = occupations
                Da = np.dot(Ca[:, :nocc_a], Ca[:, :nocc_a].T)
                Db = np.dot(Cb[:, :nocc_b], Cb[:, :nocc_b].T)
                D = Da + Db
            else:
                C = mocoeffs[0, ...]
                nocc_a, _, _, _ = occupations
                D = 2 * np.dot(C[:, :nocc_a], C[:, :nocc_a].T)
            self.gauge_origin = helpers.calculate_origin_pyscf(gauge_origin, coords, charges, D, pyscfmol, do_print=True)
        else:
            assert len(gauge_origin) == 3
            if isinstance(gauge_origin, np.ndarray):
                assert gauge_origin.flatten().shape == (3,)
            self.gauge_origin = np.asarray(gauge_origin)

    def form_operators(self):

        # angular momentum
        operator_angmom = Operator(label='angmom', is_imaginary=True, is_spin_dependent=False, triplet=False)
        self.pyscfmol.set_common_orig(self.gauge_origin)
        integrals_angmom_ao = self.pyscfmol.intor('cint1e_cg_irxp_sph', comp=3)
        operator_angmom.ao_integrals = integrals_angmom_ao
        self.driver.add_operator(operator_angmom)

        # spin-orbit (1-electron, exact nuclear charges)
        operator_spinorb = Operator(label='spinorb', is_imaginary=True, is_spin_dependent=False, triplet=False)
        integrals_spinorb_ao = 0
        for atm_id in range(self.pyscfmol.natm):
            self.pyscfmol.set_rinv_orig(self.pyscfmol.atom_coord(atm_id))
            chg = self.pyscfmol.atom_charge(atm_id)
            integrals_spinorb_ao += chg * self.pyscfmol.intor('cint1e_prinvxp_sph', comp=3)
        operator_spinorb.ao_integrals = integrals_spinorb_ao
        self.driver.add_operator(operator_spinorb)

        # spin-orbit (1-electron, effective nuclear charges)
        operator_spinorb_eff = Operator(label='spinorb_eff', is_imaginary=True, is_spin_dependent=False, triplet=False)
        integrals_spinorb_eff_ao = 0
        for atm_id in range(self.pyscfmol.natm):
            self.pyscfmol.set_rinv_orig(self.pyscfmol.atom_coord(atm_id))
            # chg = self.pyscfmol.atom_effective_charge[atm_id]
            chg = 0
            integrals_spinorb_eff_ao += chg * self.pyscfmol.intor('cint1e_prinvxp_sph', comp=3)
        operator_spinorb_eff.ao_integrals = integrals_spinorb_eff_ao
        self.driver.add_operator(operator_spinorb_eff)

    def form_results(self):

        operator_angmom = self.driver.solver.operators[0]
        # angmom_grad_alph = operator_angmom.mo_integrals_ai_supervector_alph
        # print(angmom_grad_alph[0, :, 0])
        # angmom_resp_alph = operator_angmom.rspvecs_alph[0]
        # angmom_resp_beta = operator_angmom.rspvecs_beta[0]
        # print(angmom_resp_alph.shape)
        # print(np.linalg.norm(angmom_resp_alph[0, :, 0]))
        # print(angmom_resp_beta.shape)
        # print(np.linalg.norm(angmom_resp_beta[0, :, 0]))
        operator_spinorb = self.driver.solver.operators[1]
        operator_spinorb_eff = self.driver.solver.operators[2]

        np_formatter = {
            'float_kind': lambda x: '{:14.8f}'.format(x)
        }
        # np.set_printoptions(linewidth=200, formatter=np_formatter)
        assert len(self.driver.results) == 1
        results = self.driver.results[0]
        assert results.shape == (9, 9)
        block_1 = results[0:3, 0:3] # angmom/angmom
        block_2 = results[0:3, 3:6] # angmom/spinorb
        block_3 = results[0:3, 6:9] # angmom/spinorb_eff
        block_4 = results[3:6, 0:3] # spinorb/angmom
        block_5 = results[3:6, 3:6] # spinorb/spinorb
        block_6 = results[3:6, 6:9] # spinorb/spinorb_eff
        block_7 = results[6:9, 0:3] # spinorb_eff/angmom
        block_8 = results[6:9, 3:6] # spinorb_eff/spinorb
        block_9 = results[6:9, 6:9] # spinorb_eff/spinorb_eff

        nalph, nbeta = self.pyscfmol.nelec
        exact_spin = 0.5 * (nalph - nbeta)
        res_1 = block_2 / exact_spin
        res_2 = (block_3 - block_2) / exact_spin
        res = res_1 + res_2

        # principal values are sqrt(eigvals(g.T * g)
        prin_1 = np.sqrt(np.linalg.eigvals(np.dot(res_1.T, res_1)))

        self.g_oz_soc_1 = res_1
        self.g_oz_soc_1_eig = prin_1
