import sys
import os
import unittest
import asyncore

from BaseHandler import *
from MockClient import *
from DPHandler import *

class DPLHandler(BaseHandler):
	def __init__(self, client):
		BaseHandler.__init__(self,'dpl.nate.com', 5004, client)
		
	def connected(self):
		self.send('PVER', '3.871 3.0 ko.linux\r\n')
			
	def gotPVER(self, data):
		self.send('AUTH', 'AUTH\r\n')
		
	def gotAUTH(self, data):
		self.send('REQS', 'DES %s\r\n'%(self.client.id))
		
	def gotREQS(self, data):
		tokens = data.split()
		ip = tokens[3]
		port = int(tokens[4])
		self.client.dpConnection = Connection(DPHandler(ip, port, self.client))
		self.client.dpConnection.connectToServer()
		
class DPLConnectTests(unittest.TestCase):
	def setUp(self):
		pass

	def testConnect(self):
		handler = DPLHandler(MockClient())
		connection = Connection(handler)
		connection.connectToServer()
		asyncore.loop()
		#self.assertEqual(6, len(pyteOn.groups))
		#print pyteOn.buddies

if __name__ == '__main__':
	unittest.main()