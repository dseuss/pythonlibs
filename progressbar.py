#!/usr/bin/env python
# encoding: utf-8

""" Simple progress bar for day to day use (in IPython e.g.).

TODO make python3 compatible
TODO fanzier output, javascript progress bar in IPython?

"""

from __future__ import division
import sys

def _nr_digits(number):
    return len(str(number))

class Monitor(object):

    """ Simple Progress bar for looping over iteratable object. Use as:
            for i in Monitor(...):
                do_something
        As long as there is no printing involved in do_something, you get
        a nice little progress bar.
    """
    def __init__(self, iterable, size=50):
        """

        :iterable: Iteratable object to loop over
        :size(50): Number of characters for the progress bar.
        :returns: Monitor

        """
        self._iterable = iter(iterable)
        self._total = len(iterable)
        self._size = size
        self._current = 0

    def __iter__(self):
        return self

    def next(self):
        # FIXME Make more readable
        # FIXME Make this depend on return value of self._iterable.next()
        if self._current < self._total:
            self._current += 1
            carrets = (self._current * self._size) // \
                    self._total if self._current < self._total else self._size
            statusmsg = ('{0:' + str(_nr_digits(self._total)) + '}/{1}').format(self._current, self._total)
            msg = ''.join(('[', carrets * '=', (self._size - carrets) * ' ', ']  ', statusmsg))
            print "\r" + str(msg),
            sys.stdout.flush()
        else:
            print ""

        return self._iterable.next()


if __name__ == '__main__':
    from time import sleep
    for i in Monitor(range(10)):
        sleep(1)
    for i in Monitor(range(10)):
        sleep(1)
