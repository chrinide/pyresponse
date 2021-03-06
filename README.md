# pyresponse

Molecular frequency-dependent response properties for arbitrary operators.

[![build status](http://img.shields.io/travis/cclib/cclib/master.svg?style=flat)](https://travis-ci.org/berquist/pyresponse)
[![codecov](https://codecov.io/gh/berquist/pyresponse/branch/master/graph/badge.svg)](https://codecov.io/gh/berquist/pyresponse)
[![license](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg?style=flat)](https://github.com/berquist/pyresponse/blob/master/LICENSE)

Currently, the goal is to provide:

1. a pedagogical example of a working molecular orbital response program as an almost direct translation from equations to code,
2. an implementation that gives "exact" results for testing, and
3. an example of testing and documenting scientific code using modern software development tools.

# Requirements

* Python >= 3.2 because of pyscf.
* [pyscf](https://github.com/sunqm/pyscf) and its dependencies

## Python dependencies

* [periodictable](https://github.com/pkienzle/periodictable) (for calculating the center of mass)
* [pytest](http://doc.pytest.org/en/latest/) (for testing)
* [daltools](https://github.com/vahtras/daltools) (for testing?)
* [cclib](https://github.com/cclib/cclib) (for ?)

# Testing

    make pytest

# Caveats

* RHF and UHF references only.
* Hartree-Fock and DFT only; no post-HF methods yet.
* Because the dimensioning of all arrays is based around the ov/vo space, methods that have non-zero contributions from the oo space (specifically derivatives of GIAOs/London orbitals w.r.t. the B-field) are not currently possible.
* No iterative schemes are implemented, only "exact" methods involving explicit construction of the full orbital Hessian and then inverting it (for response) or diagonalizing it (for excitation energies/transition moments/residues). Better have lots of memory!
* Linear response and single residues only.
* _unrestricted diagonalization-based properties are not implemented/working_

# Desired features (in no specific order)

* Non-orthogonal orbitals. Requires switch from using MO energies to full Fock matrices.
* ROHF reference (compare against DALTON). Requires equations for the ROHF orbital Hessian.
* Post-HF support: MP2, CCSD, and CIS. Requires constriction of a Lagrangian.
* Support for GIAOs. Only requires re-dimensioning as long as AO matrix elements are available??
* At least one iterative method for each property type, for example DIIS for inversion and Davidson for diagonalization. Requires matrix-vector products.
* Quadratic response and associated single residues (needed for phosphorescence) and double residues (excited state expectation values and transition moments of linear operators). Requires permutation of linear response solution vectors.

## Desired features that don't fix the caveats

* Open-ended response: see [Ringholm, Jonsson, and Ruud](http://dx.doi.org/10.1002/jcc.23533).
* Finite-difference for testing and higher-order response.
* Independence from pyscf, requires molecule/basis set handling, AO integral engine, and RHF/UHF solver.
* Interface to [PyQuante](https://github.com/berquist/pyquante) and/or [pyquante2](https://github.com/rpmuller/pyquante2).
* Interface to [Psi4](https://github.com/psi4/psi4) (through Python, not C++).
* Sphinx-based documentation.
* Jupyter Notebook-based tutorials.
* Argument type-checking using [mypy](http://mypy-lang.org/).

# References

Forthcoming...
