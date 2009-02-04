#!/usr/bin/env python
# encoding: utf-8
"""
Connection.py

Created by ljsking on 2009-02-04.
Copyright (c) 2009 ljsking. All rights reserved.
"""

import asyncore, socket

class Connection(asyncore.dispatcher):
	def __init__(self, commandHandler):
		asyncore.dispatcher.__init__(self)
		self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
		self.seq = 0
		self.commandHandler = commandHandler
		self.commandHandler.send = self.sendCommand
	
	def connectToServer(self):
		self.connect( (self.commandHandler.host, self.commandHandler.port) )
		self.commandHandler.connected()

	def handle_connect(self):
		pass

	def handle_close(self):
		self.close()
		print 'closed'

	def handle_read(self):
		data = self.recv(8192)
		command = data[:data.find(" ")]
		print 'command: %s'%command
		try:
			method = self.commandHandler.__getattribute__("got"+command)
			method(data)
		except AttributeError:
			print "unexpected command:%s"%command

	def writable(self):
		return (len(self.buffer) > 0)

	def handle_write(self):
		sent = self.send(self.buffer)
		self.buffer = self.buffer[sent:]

	def sendCommand(self, command, arg):
		self.buffer = '%s %d %s'%(command, self.seq, arg)
		self.seq += 1