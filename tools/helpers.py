#!/usr/bin/env python
# encoding: utf-8
"""Little helpers for everyday python workLittle helpers for everyday python work.."""

from __future__ import division

import os
import sys
from time import time

import fcntl
import termios


class Timer(object):

    """Simple timing object. Measure the system time spend in the with-block
    and prints it to stdout after completion.

    Usage:
        with Timer('Function took'):
            do_something()
    """

    def __init__(self, msg='Timer'):
        """
        :param msg: Additional message to show after finishing timing.

        """
        self._msg = msg
        self._start = None

    def __enter__(self):
        self._start = time()

    def __exit__(self, *args):
        print('{}: {}s'.format(self._msg, time() - self._start))


def _nr_digits(number):
    """Returns the string-length of `number`

    :param number: Number to measure string length
    :returns: The length of number when seen as a string
    """
    return len(str(number))


class Progress(object):

    """Progress bar for looping over iteratable object. Use as:
            for i in Monitor(...):
                do_something
    As long as there is no printing involved in do_something, you get
    a nice little progress bar. Works fine on the console as well as all
    ipython interfaces.
    """
    # TODO make python3 compatible

    def __init__(self, iterable, size=50):
        """
        :param iterable: Iteratable object to loop over
        :param size: Number of characters for the progress bar (default 50).

        """
        self._iterable = iter(iterable)
        self._total = len(iterable)
        self._size = size
        self._current = 0

    def __iter__(self):
        return self

    def next(self):
        """Fetch next object from the iterable"""
        # FIXME Make more readable
        if self._current < self._total:
            self._current += 1
            if self._current < self._total:
                carrets = (self._current * self._size) // self._total
            else:
                carrets = self._size

            statusmsg = ('{0:' + str(_nr_digits(self._total)) + '}/{1}')\
                    .format(self._current, self._total)
            msg = ''.join(('[', carrets * '=', (self._size - carrets) * ' ', ']  ', statusmsg))
            print "\r" + str(msg),
            sys.stdout.flush()
        else:
            print ""

        return self._iterable.next()


def getch():
    """Gets a single character from the console."""
    fd = sys.stdin.fileno()

    oldterm = termios.tcgetattr(fd)
    newattr = termios.tcgetattr(fd)
    newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
    termios.tcsetattr(fd, termios.TCSANOW, newattr)

    oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)

    try:
        while 1:
            try:
                c = sys.stdin.read(1)
                return c
            except IOError: pass
    finally:
        termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
        fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)
