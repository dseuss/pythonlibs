#!/usr/bin/env python
# encoding: utf-8
""""""

from __future__ import division, print_function

import base64
import hashlib
import itertools as it
import os
import pickle
import sys
import traceback
from functools import wraps
from multiprocessing import Process, Queue

from . import mkdir

CACHEDIR = '.pycache'


def processify(func):
    """Decorator to run a function as a process.  Be sure that every argument
    and the return value is *pickable*. The created process is joined, so the
    code does not run in parallel.

    Taken from https://gist.github.com/schlamar/2311116
    """

    def process_func(q, *args, **kwargs):
        try:
            ret = func(*args, **kwargs)
        except Exception:
            ex_type, ex_value, tb = sys.exc_info()
            error = ex_type, ex_value, ''.join(traceback.format_tb(tb))
            ret = None
        else:
            error = None

        q.put((ret, error))

    # register original function with different name
    # in sys.modules so it is pickable
    process_func.__name__ = func.__name__ + 'processify_func'
    setattr(sys.modules[__name__], process_func.__name__, process_func)

    @wraps(func)
    def decorated(*args, **kwargs):
        q = Queue()
        p = Process(target=process_func, args=[q] + list(args), kwargs=kwargs)
        p.start()
        p.join()
        ret, error = q.get()

        if error:
            ex_type, ex_value, tb_str = error
            message = '%s (in subprocess)\n%s' % (ex_value.message, tb_str)
            raise ex_type(message)

        return ret
    return decorated


def _hash_file(filename, blocksize=65536):
    """Hashes the given file.

    :param filename: Path to file
    :returns: Hex digest of the md5 checksum

    """
    hasher = hashlib.md5()
    with open(filename, 'rb') as infile:
        buf = infile.read(blocksize)
        while len(buf) > 0:
            hasher.update(buf)
            buf = infile.read(blocksize)

    return hasher.hexdigest()


def _args_to_dict(func, args):
    """Converts the unnamed arguments of func to a dictionary

    :param func: Function
    :param *args: Valid arguments of func as tuple
    :returns: Dictionary containing with key=argument name and
        value=value in *args

    """
    argnames = func.func_code.co_varnames[:func.func_code.co_argcount]
    return {key: val for key, val in zip(argnames, args)}


def _to_hashfilename(func, args, kwargs):
    """Computes the hashfile name for a given function (with filename argument)

    :param func: Function
    :param *args: Named arguments of func
    :param **kwargs: Keyword arguments of func
    :returns: Proposed filename

    """
    filename_pos = func.func_code.co_varnames.index('filename')
    filename = args[filename_pos]
    filehash = _hash_file(filename)
    sourcehash = _hash_file(func.func_code.co_filename)

    argdict = _args_to_dict(func, args)
    argdict.update(kwargs)
    argstr = '_'.join("{}={}".format(key, val) for key, val in argdict.iteritems())

    rawname = '_'.join((filehash, sourcehash, argstr))
    return base64.urlsafe_b64encode(rawname) + '.pkl'


def cached_filefunc(func):
    """Caches the return value for a function which contains a named argument
    `filename` for further use. This can be helpful for creating plots from
    pre-computed data with an intermediate step which still takes very long.

    The cache is considered invalid (and the value is calculated from the
    proper function) if one of the following conditions is met:
        * the file corresponding the argument `filename` has changed
        * the source file of the function called has changed
        * an argument of the function called is changed

    TODO Detect default values of keyword arguments
    FIXME This is baaaaad hackery!!!
    """
    @wraps(func)
    def decorated(*args, **kwargs):
        # First we try to read the function's return value from cache
        try:
            cfilename = _to_hashfilename(func, args, kwargs)
            with open(os.path.join(CACHEDIR, cfilename), 'rb') as cfile:
                return pickle.load(cfile)
        except IOError as exception:
            if exception.errno != os.errno.ENOENT:
                raise

        # Not there? --> Compute it and cache it for further use
        val = func(*args, **kwargs)

        mkdir(CACHEDIR)
        cfilename = _to_hashfilename(func, args, kwargs)
        with open(os.path.join(CACHEDIR, cfilename), 'wb') as cfile:
            pickle.dump(val, cfile)
        return val

    if 'filename' in func.func_code.co_varnames[:func.func_code.co_argcount]:
        return decorated
    else:
        return func
