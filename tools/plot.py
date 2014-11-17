#!/usr/bin/env python
# encoding: utf-8
"""Tools making everyday plotting tasks easier."""

from __future__ import division, print_function
import numpy as np
from matplotlib import pyplot as pl


def plot(function, intervall, num=500, axis=None, **kwargs):
    """Plots the function f on the axisis axis on the intervall (xmin, xmaxis)

    :param function: Functions or list of function to plot
    :param intervall: Intervall to plot function on (xmin, xmaxis)
    :param num: Number of points used for the plot (default 500)
    :param axis: Axis to plot on (default current axisis)
    :returns: Plot (or list of plots)

    """
    if hasattr(function, '__iter__'):
        return [plot(f, intervall, num, axis, **kwargs) for f in function]
    else:
        x = np.linspace(*intervall, num=num)
        axis = pl.gca() if axis is None else axis
        return axis.plot(x, function(x), **kwargs)


def imshow(img, ax=None, **kwargs):
    """Shows the image `img` passed as numpy array in a much prettier way

    :param np.ndarray img: Image to show passed as RGB or grayscale image

    """
    ax = ax if ax is not None else pl.gca()
    ax.grid(False)
    ax.set_xticklabels([])
    ax.set_yticklabels([])

    pl.imshow(img, **kwargs)
    pl.axis((0, img.shape[1], img.shape[0], 0))
    pl.show()
