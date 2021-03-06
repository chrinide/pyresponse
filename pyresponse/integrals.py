import os
import math

import numpy as np

STARS = '********'


def read_binary(binaryfilename):
    """Return the bytes present in the given binary file name.
    """

    with open(binaryfilename, 'rb') as binaryfile:
        readbytes = binaryfile.read()

    return readbytes


def parse_aoproper(integralfilename):
    """Parse the AOPROPER file generated by DALTON and save the integral
    matrices to disk if asked.
    """

    integral_dict = dict()

    # Specify the encoding explicitly, so there's no confusion.
    encoding = 'utf-8'

    # There are a few labels we want to ignore.
    labels_to_ignore = (
        'HUCKOVLP',
        'HUCKEL',
        'HJPOPOVL',
        'EOFLABEL',
    )

    # For now, we naively read the whole file into memory, split
    # directly on the delimiter, *then* iterate. This will eventually
    # have to be changed over to a more memory-efficient version in
    # order to deal with hundreds of basis functions (if we ever want
    # that).
    integralfile_bytes = read_binary(integralfilename)
    # Remove b' \x00\x00\x00********' -> 12 bytes
    integralfile_bytes = integralfile_bytes[12:]
    integralfile_records = integralfile_bytes.split(STARS.encode(encoding=encoding))

    for record in integralfile_records:

        full_label = record[8:24].decode(encoding=encoding)
        # The first part shows the structure of the matrix.
        #  SQUARE   -> stored as the full N^2 matrix
        #  SYMMETRI -> stored as lower triangle with N*(N+1)/2 elements,
        #              ordered by rows
        #  ANTISYMM -> stored as lower triangle with N*(N+1)/2 elements,
        #              ordered by rows, (make the top triangle negative?)
        # The second part is the actual label
        # that would appear in the output file.
        shape, label = full_label[:8].strip(), full_label[8:].strip()

        # There are a few labels we want to ignore.
        if not any(label in x for x in labels_to_ignore):
            # top: b'1 A  15 ANTISYMMXDIPVEL  \x00\x00\x00\xa8\x00\x00\x00'
            # end: b'\xa8\x00\x00\x00 \x00\x00\x00' -> (168, 32)
            integrals_as_bytes = record[32:-8]
            # pylint: disable=no-member
            integrals_tril = np.fromstring(integrals_as_bytes, dtype=np.double)
            # positive solution to x = n*(n+1)/2
            nbasis = int(0.5 * (-1 + np.sqrt(1 + (8 * len(integrals_tril)))))
            # print(shape, label, len(integrals_as_bytes), nbasis, integrals_tril.shape)

            # form the full "square" matrix representation
            integrals_square = np.zeros(shape=(nbasis, nbasis))
            tril_indices = np.tril_indices(nbasis)
            integrals_square[tril_indices] = integrals_tril
            diag = np.diag(integrals_square) * np.eye(nbasis)
            if shape == 'SYMMETRI':
                integrals_square = -diag + integrals_square + integrals_square.T
            elif shape == 'ANTISYMM':
                integrals_square = -diag + integrals_square - integrals_square.T
                # If the integrals are antisymmetrized, the whole
                # thing should sum to zero.
                asum = abs(np.sum(integrals_square))
                assert asum < 1.0e-10
            else:
                print("Shouldn't be here.")

            # Was the (anti)symmetrization done correctly?
            assert integrals_square[tril_indices].all() == integrals_tril.all()

            record_dict = {
                'label': label,
                'nbasis': nbasis,
                'shape': shape,
                'integrals': integrals_square,
            }
            integral_dict[label] = record_dict

    return integral_dict

if __name__ == '__main__':
    dalton_integrals = parse_aoproper('r_lih_hf_sto-3g/dalton_response_rpa_singlet/AOPROPER')
    from .utils import dalton_label_to_operator
    labels = dalton_integrals.keys()
    for label in labels:
        print(dalton_label_to_operator(label))
