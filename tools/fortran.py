#!/usr/bin/env python
# encoding: utf-8

from __future__ import division, print_function


def str_complex(c, kindstr=''):
    """Converts the complex number `c` to a string in Fortran-format, i.e.
    (Re c, Im c). If c is iterable, it returns a string of the form
    [(Re c_1, Im c_1), ...].

    :param c: Number/Iterable to print
    :param kindstr: Additional kind qualifier to append (default None)
    :returns: String in Fortran format

    >>> str_complex(1)
    (1.0, 0.0)
    >>> str_complex(np.array([1.j, 1]))
    [(0.0, 1.0), (1.0, 0.0)]
    >>> str_complex(1, kindstr='_dp')
    (1.0_dp, 0.0_dp)
    >>> str_complex(np.array([1.j, 1]), kindstr='_sp')
    [(0.0_sp, 1.0_sp), (1.0_sp, 0.0_sp)]

    """
    if hasattr(c, '__iter__'):
        return '[' + ', '.join([str_complex(c_i, kindstr) for c_i in c]) + ']'
    else:
        c = complex(c)
        return '({}{}, {}{})'.format(c.real, kindstr, c.imag, kindstr)

if __name__ == '__main__':
    import doctest
    doctest.testmod()
