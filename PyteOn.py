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
import asyncore
import socket
import logging

from DPHandler import *
from DPLHandler import *

logging.basicConfig(level=logging.DEBUG, format="%(created)-15s %(levelname)8s %(thread)d %(name)s %(message)s")

class PyteOn:
	def __init__(self):
		self.groups = {}
		self.buddies = {}
	def connect(self, id, password):
		self.id = id
		self.password = password
		s = socket(AF_INET, SOCK_STREAM)
		s.connect(('dpl.nate.com', 5004))
		dplHandler = DPLHandler(s, self)
		asyncore.loop()
	def send_message(to, msg):
		pass

class PyteOnTests(unittest.TestCase):
	def setUp(self):
		pass
		
	def testConnect(self):
		pyteOn = PyteOn()
		pyteOn.connect('ljsking@netsgo.com', 'rjseka')

if __name__ == '__main__':
	unittest.main()