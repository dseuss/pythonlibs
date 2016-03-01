
# encoding: utf-8
"""Routines for sampling from the Haar measures of the classical compact
groups. Algorithms taken from http://arxiv.org/abs/math-ph/0609050.

TODO Symplectic groups are missing
"""

from __future__ import division, print_function
import numpy as np
from scipy.linalg import qr, eigvals


def orthogonal(dim, randn=np.random.randn):
    """Returns a sample from the Gaussian orthogonal ensemble of given
    dimension.  (i.e. the haar measure on U(dim)).

    :param int dim: Dimension
    :param randn: Function to create real N(0,1) distributed random variables.
        It should take the shape of the output as numpy.random.randn does
        (default: numpy.random.randn)
    """
    z = randn(dim, dim)
    q, r = qr(z)
    d = np.diagonal(r)
    ph = d / np.abs(d)
    return q * ph


def unitary(dim, randn=np.random.randn):
    """Returns a sample from the Gaussian unitary ensemble of given dimension.
    (i.e. the haar measure on U(dim)).

    :param int dim: Dimension
    :param randn: Function to create real N(0,1) distributed random variables.
        It should take the shape of the output as numpy.random.randn does
        (default: numpy.random.randn)
    """
    z = (randn(dim, dim) + 1j * randn(dim, dim)) / np.sqrt(2.0)
    q, r = qr(z)
    d = np.diagonal(r)
    ph = d / np.abs(d)
    return q * ph


#############
#  Tesing   #
#############
LEVEL_SPACING_DF = {'orthogonal': lambda s: np.pi / 2 * s * np.exp(-np.pi / 4 * s**2),
                    'unitary': lambda s: 32 / np.pi**2 * s**2 * np.exp(-4 / np.pi * s**2)
                    }


def _test_ensemble(dim, ensemble, samples=1000):
    import matplotlib
    matplotlib.use('TkAgg')
    from matplotlib import pyplot as pl
    from tools.helpers import Progress

    eigdists = []
    get_sample = globals()[ensemble]
    for _ in Progress(xrange(samples)):
        u = get_sample(dim)
        eigs = np.sort(np.angle(eigvals(u)))
        eigdists += list(eigs[1:] - eigs[:-1])

    eigdists = np.asarray(eigdists) / (np.sum(eigdists) / len(eigdists))
    pl.hist(eigdists, bins=50, normed=True)
    dist = lambda s: 32 / np.pi**2 * s**2 * np.exp(-4 / np.pi * s**2)
    s = np.linspace(0, 4, 100)
    pl.plot(s, dist(s))
    pl.show()

if __name__ == '__main__':
    _test_ensemble(50, 'unitary', samples=10000)
    _test_ensemble(50, 'orthogonal', samples=10000)
