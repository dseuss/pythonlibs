#!/usr/bin/env python
# encoding: utf-8

from __future__ import division, print_function
import numpy as np

SI = np.eye(2)
SX = np.array([[0, 1], [1, 0]])
SY = np.array([[0, 1j], [-1j, 0]])
SZ = np.array([[1, 0], [0, -1]])
SP = 0.5 * (SX + 1j * SY)
SM = 0.5 * (SX - 1j * SY)
PAULI = np.asarray([SI, SX, SY, SZ])
