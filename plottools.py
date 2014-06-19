"""Tools making everyday plotting tasks easier."""
#!/usr/bin/env python
# encoding: utf-8

from __future__ import division, print_function
import numpy as np
import matplotlib.pyplot as pl


def plot(function, intervall, num=500, axis=None, **kwargs):
    """Plots the function f on the axisis axis on the intervall (xmin, xmaxis)

    function  -- Functions or list of function to plot
    intervall -- Intervall to plot function on (xmin, xmaxis)

    Keyword arguments:
    num -- Number of points used for the plot (default 500)
    axis        -- Axis to plot on (default current axisis)

    Returns:
    Plot (or list of plots)
    """
    if hasattr(function, '__iter__'):
        return [plot(f, intervall, num, axis, **kwargs) for f in function]
    else:
        x = np.linspace(*intervall, num=num)
        axis = pl.gca() if axis is None else axis
        return axis.plot(x, function(x), **kwargs)
