#!/usr/bin/env python
# encoding: utf-8
"""
PyteOn.py

Created by ljsking on 2009-02-03.
Copyright (c) 2009 ljsking. All rights reserved.
"""

import sys
import os
import unittest

from DPConnect import *
from DPLConnect import *

class PyteOn:
	def __init__(self):
		pass
	def connect(self, id, password):
		self.id = id
		self.password = password
		self.dplConnect = DPLConnect(self)
		self.dplConnect.connect()

class PyteOnTests(unittest.TestCase):
	def setUp(self):
		pass
		
	def testConnect(self):
		pyteOn = PyteOn()
		pyteOn.connect('ljsking@netsgo.com', 'rjseka')

if __name__ == '__main__':
	unittest.main()