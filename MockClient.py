#!/usr/bin/env python
# encoding: utf-8
"""
MockClient.py

Created by ljsking on 2009-02-04.
Copyright (c) 2009 __MyCompanyName__. All rights reserved.
"""

import sys
import os
import unittest

class MockClient:
	id = "ljsking@netsgo.com"
	password = "rjseka"
	def __init__(self):
		self.groups = {}
		self.buddies = {}