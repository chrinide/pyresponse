import os.path

import pyscf


__filedir__ = os.path.realpath(os.path.dirname(__file__))
refdir = os.path.join(__filedir__, 'reference_data')


def molecule_water_sto3g(verbose=0):

    mol = pyscf.gto.Mole()
    mol.verbose = verbose
    mol.output = None

    with open(os.path.join(refdir, 'water.xyz')) as fh:
        mol.atom = fh.read()
    mol.basis = 'sto-3g'
    mol.charge = 0
    mol.spin = 0

    mol.unit = 'Bohr'

    return mol


def molecule_glycine_sto3g(verbose=0):

    mol = pyscf.gto.Mole()
    mol.verbose = verbose
    mol.output = None

    with open(os.path.join(refdir, 'glycine.xyz')) as fh:
        next(fh)
        next(fh)
        mol.atom = fh.read()
    mol.basis = 'sto-3g'
    mol.charge = 0
    mol.spin = 0

    return mol


def molecule_trithiolane_sto3g(verbose=0):

    mol = pyscf.gto.Mole()
    mol.verbose = verbose
    mol.output = None

    with open(os.path.join(refdir, 'trithiolane.xyz')) as fh:
        next(fh)
        next(fh)
        mol.atom = fh.read()
    mol.basis = 'sto-3g'
    mol.charge = 0
    mol.spin = 0

    return mol


def hydrogen_atom_sto3g(verbose=0):

    mol = pyscf.gto.Mole()
    mol.verbose = verbose
    mol.output = None

    mol.atom = [
        ['H' , (0.0, 0.0, 0.0)]
    ]
    mol.basis = 'sto-3g'
    mol.charge = 0
    mol.spin = 1

    return mol


def molecule_bc2h4_cation_sto3g(verbose=0):

    mol = pyscf.gto.Mole()
    mol.verbose = verbose
    mol.output = None

    with open(os.path.join(refdir, 'BC2H4.xyz')) as fh:
        next(fh)
        next(fh)
        mol.atom = fh.read()
    mol.basis = 'sto-3g'
    mol.charge = 1
    mol.spin = 0

    return mol


def molecule_bc2h4_neutral_radical_sto3g(verbose=0):

    mol = molecule_bc2h4_cation_sto3g(verbose)
    mol.charge = 0
    mol.spin = 1

    return mol


def molecule_lih_cation_sto3g(verbose=0):

    mol = pyscf.gto.Mole()
    mol.verbose = verbose
    mol.output = None

    with open(os.path.join(refdir, 'LiH.xyz')) as fh:
        next(fh)
        next(fh)
        mol.atom = fh.read()
    mol.basis = 'sto-3g'
    mol.charge = 1
    mol.spin = 1

    return mol


def molecule_0w4a_dication_321g(verbose=0):

    mol = pyscf.gto.Mole()
    mol.verbose = verbose
    mol.output = None

    with open(os.path.join(refdir, '0w4a.xyz')) as fh:
        next(fh)
        next(fh)
        mol.atom = fh.read()
    mol.basis = '3-21g'
    mol.charge = 2
    mol.spin = 1

    return mol


def molecule_bh_cation_def2_svp(verbose=0):

    mol = pyscf.gto.Mole()
    mol.verbose = verbose
    mol.output = None

    mol.atom = [
        ['B', (0.0000, 0.0000, 0.0000)],
        ['H', (0.0000, 0.0000, 1.2340)],
    ]
    mol.basis = 'def2-svp'
    mol.charge = 1
    mol.spin = 1

    return mol
