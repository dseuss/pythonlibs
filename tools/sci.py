#!/usr/bin/env python
# encoding: utf-8

from __future__ import division, print_function
import numpy as np
from scipy.integrate import ode


def zodeint(func, y0, t, **kwargs):
    """Simple wraper around scipy.integrate.ode for complex valued problems.

    :param func: Right hand side of the equation dy/dt = f(t, y)
    :param y0: Initial value at t = t[0]
    :param t: Sequence of time points for whihc to solve for y
    :returns: y[len(t), len(y0)]

    """
    y0 = np.array([y0]) if np.isscalar(y0) else y0
    integrator = ode(func) \
            .set_integrator('zvode', with_jacobian=False, **kwargs) \
            .set_initial_value(y0)

    y = np.empty((len(t), len(y0)), dtype=complex)
    y[0] = y0

    for i in xrange(1, len(t)):
        integrator.integrate(t[i])
        if not integrator.successful():
            print('WARNING: Integrator failed')
            break
        y[i] = integrator.y

    return t[:i+1], y[:i+1]
