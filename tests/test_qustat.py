import pytest
import numpy as np
import scipy.sparse as sp
from itertools import product

import physics.qustat as qs


@pytest.mark.parametrize("nr_fermions", range(1, 10))
def test_annhilators(nr_fermions):
    annh = qs.annhilation_operators(nr_fermions)

    anticomm = lambda A, B: A * B + B * A
    iszero = lambda A: A.nnz == 0
    isiden = lambda A: (A != sp.identity(A.shape[0])).nnz == 0

    for i, j in product(range(nr_fermions), range(nr_fermions)):
        if i == j:
            assert isiden(anticomm(annh[i], annh[j].conj().T))
        else:
            assert iszero(anticomm(annh[i], annh[j].conj().T))

        assert iszero(anticomm(annh[i], annh[j]))


@pytest.mark.parametrize("dim", range(2, 4))
def test_embed(dim):
    idm = np.identity(dim)
    op = np.random.rand(dim, dim)
    assert (qs.embed(op, 0, 3) == qs.tensor((op, idm, idm))).all()
    assert (qs.embed(op, 1, 3) == qs.tensor((idm, op, idm))).all()
    assert (qs.embed(op, 2, 3) == qs.tensor((idm, idm, op))).all()
