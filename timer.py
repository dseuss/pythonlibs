#!/usr/bin/env python
# encoding: utf-8

from __future__ import division, print_function
from time import time


class Timer(object):

    """ Simple timing object.

    Usage:
        with Timer('Function took'):
            do_something()
    """

    def __init__(self, msg='Timer'):
        """
        :msg: Additional message to show after finishing timing.

        """
        self._msg = msg
        self._start = None

    def __enter__(self):
        self._start = time()

    def __exit__(self, *args):
        print('{}: {}s'.format(self._msg, time() - self._start))
