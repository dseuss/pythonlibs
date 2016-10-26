#!/usr/bin/env python
# encoding: utf-8
"""Little helpers for everyday python workLittle helpers for everyday python work.."""

from __future__ import division

import os
import subprocess
import sys
import time
import progressbar as pb
from progressbar import ProgressBar
from collections import Sequence, Iterator, Iterable

import fcntl
import termios
from itertools import islice


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
        self._start = time.time()

    def __exit__(self, *args):
        print('{}: {}s'.format(self._msg, time.time() - self._start))


def _nr_digits(number):
    """Returns the string-length of `number`

    :param number: Number to measure string length
    :returns: The length of number when seen as a string
    """
    return len(str(number))


class CountSlice(Iterable):
    """Docstring for CountSlice. """

    def __init__(self, iterable, steps):
        """@todo: to be defined1.

        :param iterable: @todo
        :param steps: @todo

        """
        self._iterable = iterable
        self._steps = steps

    def __len__(self):
        try:
            return min(len(self._iterable), self._steps)
        except TypeError:
            return self._steps

    def __iter__(self):
        return islice(self._iterable, self._steps)


class RuntimeSlice(Iterable):
    """Docstring for RuntimeSlice. """

    def __init__(self, iterable, runtime):
        """@todo: to be defined1.

        :param iterable: @todo
        :param runtime: @todo

        """
        self._iterable = iterable
        self._runtime = runtime

    @property
    def runtime(self):
        return self._runtime

    def __iter__(self):
        starttime = time.time()
        for val in self._iterable:
            runtime = time.time() - starttime
            yield runtime, val
            if runtime > self.runtime:
                raise StopIteration()


def Progress(the_iterable, *args, **kwargs):
    if isinstance(the_iterable, RuntimeSlice):
        return TimelyProgress(the_iterable, *args, **kwargs)
    else:
        return CountProgress(the_iterable, *args, **kwargs)


class TimelyProgress(ProgressBar, Iterable):
    """Progress bar for looping over iteratable object. Use as:
            for i in Monitor(...):
                do_something
    As long as there is no printing involved in do_something, you get
    a nice little progress bar. Works fine on the console as well as all
    ipython interfaces.
    """

    def __init__(self, iterable, *args, rettime=False, **kwargs):
        """
        :param iterable: Iteratable object to loop over
        :param size: Number of characters for the progress bar (default 50).

        """
        maxtime = time.strftime("%H:%M:%S", time.gmtime(iterable.runtime))
        super().__init__(*args, max_value=iterable.runtime,
                         widgets=[pb.Percentage(), ' ', pb.Bar(), ' ',
                                  pb.Timer(), ' / ', maxtime],
                         **kwargs)
        self._iterable = iterable
        self._rettime = rettime

    def __iter__(self):
        """Fetch next object from the iterable"""
        self.start()
        for runtime, val in self._iterable:
            self.update(min(runtime, self._iterable.runtime))
            yield val if not self._rettime else (runtime, val)
        self.finish()


class CountProgress(ProgressBar, Iterable):
    """Progress bar for looping over iteratable object. Use as:
            for i in Monitor(...):
                do_something
    As long as there is no printing involved in do_something, you get
    a nice little progress bar. Works fine on the console as well as all
    ipython interfaces.
    """

    def __init__(self, iterable, *args, **kwargs):
        """
        :param iterable: Iteratable object to loop over
        :param size: Number of characters for the progress bar (default 50).

        """
        if 'max_value' not in kwargs:
            kwargs['max_value'] = len(iterable) if hasattr(iterable, '__len__')\
                else None

        super().__init__(*args, **kwargs)
        self._iterable = iterable

    def __iter__(self):
        """Fetch next object from the iterable"""
        self.start()
        for n, val in enumerate(self._iterable):
            self.update(n)
            yield val


class AsyncTaskWatcher(object):
    def __init__(self):
        self._tasks = []

    def append(self, task):
        self._tasks.append(task)

    def block(self):
        try:
            bar = ProgressBar(max_value=sum(len(t) for t in self._tasks))
            bar.start()
            while not all(t.done() for t in self._tasks):
                bar.update(value=sum(t.progress for t in self._tasks))
                time.sleep(1)
            bar.finish()
        except KeyboardInterrupt:
            pass


def watch_async_view(task):
    watcher = AsyncTaskWatcher()
    watcher.append(task)
    watcher.block()


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
            except IOError:
                pass
    finally:
        termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
        fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)


def get_git_revision_hash():
    return subprocess.check_output(['git', 'rev-parse', 'HEAD']).split()[0]


def get_git_revision_short_hash():
    return subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).split()[0]


def mkdir(dirname):
    """Create dir if it doesnt exist."""
    try:
        os.makedirs(dirname)
    except OSError as exception:
        if exception.errno != os.errno.EEXIST:
            raise
