#!/usr/bin/env python
# encoding: utf-8
"""
Buddy.py

Created by ljsking on 2009-02-03.
Copyright (c) 2009 ljsking. All rights reserved.
"""

import sys
import os
import unittest


class Buddy:
	def __init__(self, name, nick, email, group):
		self.name = name
		self.nick = nick
		self.email = email
		self.group = group


class BuddyTests(unittest.TestCase):
	def setUp(self):
		pass


if __name__ == '__main__':
	unittest.main()