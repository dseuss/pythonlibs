#!/usr/bin/env python
"""Rountines to deal with quantum statistics of bosons and fermions"""

from __future__ import division, print_function
import numpy as np
import scipy.sparse as sp


#############################################
#  Distinguishable manybody quantum sytems  #
#############################################
def tensor(xs, kronfun=np.kron):
    """Compute the vector represenation of the tensor product

                        xs[0] * xs[1] *  ... * xs[-1].

    :param xs: List of vectors
    :param kronfun: Kronecker product implementation to use (default np.kron)
    :returns: Vector of size prod_j len(xs[j])

    """
    res = np.asarray([1])
    for x in xs:
        res = kronfun(x, res)
    return res


def embed(op, pos, full_space, kronfun=np.kron, identity=np.identity):
    """Returns the matrix representaion of the embeding

                    I * ... * I * op * I ... * I

    for the operator `op` in a larger product Hilbert space. The total space
    is determined by `full_space`:
        - if `full_space` is list-like, the i-th entry of `full_space` gives
          the dimension of the i-th factor space.
        - otherwise we assume `full_space` is a number giving the total number
          of factor spaces, where each has the same dimension as the space
          `op` is acting on

    :param op: n*n array; the operator to be embeded
    :param pos: integer; the factor space in which `op` is embeded
    :param full_space: either list-like; each entry gives the dimension of the
                       respective factor space. Then we need to have
                            full_space[pos] == op.shape[0]
                       or integer; total number of factor spaces, then
                            full_space > pos
    :param kronfun: Kronecker product implementation to use (default np.kron)
    :param identity: Identity-matrix implementation (default np.identity)
    :returns: Array of size prod_j full_space[j] (or op.shape[0]^full_space)

    """
    # If we dont pass a dimension list, create one and call again
    if not hasattr(full_space, '__iter__'):
        dims = (np.shape(op)[0],) * full_space
        return embed(op, pos, dims, kronfun, identity)

    if np.shape(op)[0] != full_space[pos]:
        raise IndexError("qustat.py:embed: Dimensions do not match.")

    idmatrices = [identity(dim) for dim in full_space]
    return tensor(idmatrices[:pos] + [op] + idmatrices[pos + 1:], kronfun)


######################################
#  Bosonic manybody quantum systems  #
######################################
def symmtensor(xs):
    """Compute vector representation of the symmetrized tensor product

              1/n! * sum_p (xs[p_0] * xs[p_1] * ... * xs[p_n])

    where the sum extends over all permutations of [1..n]
    :param xs: Array-like of n vectors of idendical size
    :returns: Vector of size len(xs[0])^n

    """
    permutations = _permute(range(len(xs)))
    return sum([tensor(xs[list(sigma)]) for sigma, _ in permutations]) / \
            len(permutations)


########################################
#  Fermionic manybody quantum systems  #
########################################
def _permute(seq):
    """Returns all permutations and the signature of these permutations
    of the sequence `seq`.

    :param seq: Iteratable
    :returns: List of permutations, corresponding signature

    Taken from http://rosettacode.org/wiki/Permutations_by_swapping#Python
    """
    items = [[]]
    for j in seq:
        new_items = []
        for i, item in enumerate(items):
            if i % 2:
                # step up
                new_items += [item[:i] + [j] + item[i:]
                              for i in range(len(item) + 1)]
            else:
                # step down
                new_items += [item[:i] + [j] + item[i:]
                              for i in range(len(item), -1, -1)]
        items = new_items

    return {(tuple(item), -1 if i % 2 else 1) for i, item in enumerate(items)}


def wedgetensor(xs):
    """Compute the vector representation wedge product (antisymmetrized
    tensor product)

        xs[0] ^ xs[1] ^ ... ^ xs[n]
                = 1/n! * sum_p sign(p) * (xs[p_0] * xs[p_1] * ... * xs[p_n])

    where the sum extends over all permutations of [1..n] and sign(p) is the
    permutation's signature.

    :param xs: Array-like of n vectors of identical size
    :returns: Vector of size len(xs[0])^n

    """
    permutations = _permute(range(len(xs)))
    return sum([sign * tensor(xs[list(sigma)])
                for sigma, sign in permutations]) / len(permutations)


def annhilation_operators(nr_fermions):
    """Compute the sparse-matrix representations of the annhilators d_j of
    a `nr_fermions` fermion system. Due to the cannonical anticommutator
    relations {d_i, adj(d)_j} = delta_ij, the matrix elements in the basis

                (|0,0,...,0> , |1,0,...,0>, ..., |1,...,1,1>),

    where (let N = `nr_fermions`)

            |n_1,...,n_N> = adj(d)_1^n_1 ... adj(d)_N^n_N |0,0,...,0>,

    have to be calculated as Kronecker products

                d_j = eta * eta * ... * d * I * ... * I.

    Here, I = diag(1, 1); eta = diag(1, -1); and d = ((0, 1), (0, 0)).

    :param nr_fermions: Number of fermions to consider
    :returns: List of length N, where the n-th entry is the sparse matrix
              representation of d_n

    """
    iden = sp.identity(2)
    eta = sp.spdiags([[1, -1]], [0], 2, 2)
    annh = sp.csr_matrix([[0, 1], [0, 0]])
    res = [tensor([eta]*n + [annh] + [iden]*(nr_fermions-1-n), sp.kron).tocsr()
           for n in range(nr_fermions)]

    for A in res:
        A.eliminate_zeros()
    return res
