#!/usr/bin/env python
# encoding: utf-8
"""Tools making everyday plotting tasks easier."""

from __future__ import division, print_function

from itertools import izip
from matplotlib import pyplot as pl

import numpy as np


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


def _imshow_formater(arr):
    """Creates a formating function to show the values of imshow in the status
    bar.

    :param arr: Array to be shown
    :returns: function formater(x, y) that should be set to ax.format_coord

    """
    def format_coord(x, y):
        col, row = int(x + .5), int(y + .5)
        if (col >= 0) and (col < arr.shape[1]) \
                and (row >= 0) and (row < arr.shape[0]):
            return "x={}, y={}, val={}".format(col, row, arr[row, col])
        else:
            return "x={}, y={}".format(col, row)
    return format_coord


def imshow(img, ax=None, show=True, **kwargs):
    """Shows the image `img` passed as numpy array in a much prettier way

    :param np.ndarray img: Image to show passed as RGB or grayscale image
    :param ax: Axis to use for plot (default: current axis)
    :param bool show: Whether to call pl.show() afterwards
    :param kwargs: Keyword arguments passed to imshow

    """
    if ax is None:
        ax = pl.gca()

    ax.grid(False)
    # ax.set_xticklabels([])
    # ax.set_yticklabels([])

    res = ax.imshow(img, **kwargs)
    ax.axis((-.5, img.shape[1] - .5, img.shape[0] - .5, -.5))
    ax.format_coord = _imshow_formater(img)
    if show:
        pl.show()
    return res


def imsshow(imgs, layout='h', show=True, **kwargs):
    """Plots a grid of images

    :param imgs: List of images as 2D arrays
    :param layout: 'h' for horizontal layout; 'v' for vertical
    :param bool show: Whether to call pl.show() afterwards
    :param kwargs: Keyword arguments passed to imshow
    :returns: List of axes

    """
    if layout == 'h':
        axlist = [pl.subplot(1, len(imgs), i + 1) for i in range(len(imgs))]
    elif layout == 'v':
        axlist = [pl.subplot(len(imgs), 1, i + 1) for i in range(len(imgs))]
    else:
        raise AttributeError(str(layout) + " is not a valid layout.")

    for ax, img in izip(axlist, imgs):
        imshow(img, ax=ax, show=False, **kwargs)
        ax.format_coord = _imshow_formater(img)

    if show:
        pl.show()

    return axlist


def rgb2gray(img):
    """Converts a RGB encoded image to grayscale

    :param img: n-dim Array, with the last dimension of size 3 encoding RGB
    :returns: (n-1) dim Array of shape img.shape[:-1]

    """
    return np.dot(img, (0.2989, 0.5870, 0.1140))
