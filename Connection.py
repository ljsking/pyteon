#!/usr/bin/env python
# encoding: utf-8
"""
Connection.py

Created by ljsking on 2009-02-04.
Copyright (c) 2009 __MyCompanyName__. All rights reserved.
"""

import sys
import os
import unittest


class Connection(asyncore.dispatcher):
	def __init__(self, commandHandler):
		asyncore.dispatcher.__init__(self)
		self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
		self.connect( ('dpl.nate.com', 5004) )
		self.seq = 0
		self.sendCommand('PVER', '3.871 3.0 ko.linux\r\n')
		self.commandHandler = commandHandler
		self.commandHandler.send = self.sendCommand

	def handle_connect(self):
		pass

	def handle_close(self):
		self.close()

	def handle_read(self):
		data = self.recv(8192)
		command = data[:data.find(" ")]
		print 'command: %s'%command
		#try:
		method = self.commandHandler.__getattribute__("got"+command)
		method(data)
		#except AttributeError:
		#	print data

	def writable(self):
		return (len(self.buffer) > 0)

	def handle_write(self):
		sent = self.send(self.buffer)
		self.buffer = self.buffer[sent:]

	def sendCommand(self, command, arg):
		self.buffer = '%s %d %s'%(command, self.seq, arg)
		self.seq += 1


class ConnectionTests(unittest.TestCase):
	def setUp(self):
		pass


if __name__ == '__main__':
	unittest.main()