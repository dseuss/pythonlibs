#!/usr/bin/env python
# encoding: utf-8

from __future__ import division, print_function

from time import sleep

import progressbar as pb
from IPython.utils.io import rprint


def wait_interactive(job):
    """Same as IPython.parallel.client.view.LoadBalancedView.wait_interactive
    but prints a Progressbar to both, the Notebook and the stdout of the kernel

    :param job: A ipython parallel job, should have members ready(), progress
            and __len__

    """
    widgets = [pb.Percentage(), ' ', pb.Bar(), ' ', pb.ETA()]
    bar = pb.ProgressBar(maxval=len(job), widgets=widgets)
    bar.start()

    while not job.ready():
        sleep(1)
        bar.update(job.progress)
        rprint("\r\x1b[31m" + bar._format_line() + "\x1b[0m", end="")

    bar.finish()
    rprint("\r\x1b[31m" + bar._format_line() + "\x1b[0m", end="")
