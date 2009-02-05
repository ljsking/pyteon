import sys
import os
import unittest
import asyncore
import logging

from BaseHandler import *
from socket import *
from DPHandler import *

log						= logging.getLogger(__name__)

class DPLHandler(BaseHandler):
	def __init__(self, conn_sock, client):
		BaseHandler.__init__(self, conn_sock, client)
		self.send_data('PVER', '3.871 3.0 ko.linux')
		
	def found_terminator(self):
		data = self.ibuffer
		self.ibuffer = ''
		command = data[:data.find(" ")]
		log.debug("command is " + command)
		method = 'got' + command
		if hasattr(self,method):
			getattr(self,method)(data)
		
	def gotPVER(self, data):
		log.debug("call gotPVER")
		self.send_data('AUTH', 'AUTH')
		
	def gotAUTH(self, data):
		log.debug("call gotAUTH")
		self.send_data('REQS', 'DES %s'%self.client.id)
		
	def gotREQS(self, data):
		log.debug("call gotREQS")
		
		tokens = data.split()
		host = tokens[3]
		port = int(tokens[4])
		s = socket(AF_INET, SOCK_STREAM)
		s.connect((host, port))
		handler = DPHandler(s, self.client)
