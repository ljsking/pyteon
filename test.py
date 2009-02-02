# -*- coding: utf-8 -*- 
import unittest
from Connect import *
from DPLConnect import *
from DPConnect import *
class TestSequenceFunctions(unittest.TestCase):
	id = "ljsking@netsgo.com"
	password = "rjseka"
	def setUp(self):
		self.con = Connect('ljsking@netsgo.com','rjseka')

	def connected(self, ip, port):
		self.ip = ip
		self.port = port
		
	def testConnectToDPL(self):
		dplConnect = DPLConnect(self.id, self.connected)
		dplConnect.connect()
		self.assertNotEqual(None, self.ip)
		self.assertNotEqual(None, self.port)
		
	def testTokenize(self):
		self.assertEqual('ljsking', 'ljsking@netsgo.com'.split('@')[0])
		m = md5.new()
		m.update("rjseka")
		m.update("ljsking")
		digest = m.digest()
		self.assertEqual(16, len(digest))
		data = ''
		for a in digest:
			data += '%02x'%ord(a)
		self.assertEqual(32, len(data))
		
	def testConnectToDP(self):
		dplConnect = DPLConnect(self.id, self.connected)
		dplConnect.connect()
		dpConnect = DPConnect(self.id, self.password, self.ip, self.port)
		dpConnect.connect()
		
	def testParseByNewLine(self):
		data = 'test\r\ntest'
		tokens = data.split('\r\n')
		self.assertEqual(2, len(tokens))
		data = 'test\r\ntest\r\n'
		tokens = data.split('\r\n')
		self.assertEqual(3, len(tokens))
		self.assertEqual('', tokens[2])
		
	def getData(self):
		self.counting+=1
		if 1 == self.counting:
			return 'AUTH 2 AUTH\r\ntest'
		elif 2 == self.counting:
			return '2\r\ntest3\r\n'
		elif 3 == self.counting:
			return 'test4\r\ntest5\r\n'
		else:
			return
			
	def parseReceiveData(self):
		data = ''
		self.counting = 0
		while(True):
			data += self.getData()
			tokens = data.split('\r\n')
			for idx in range(0, len(tokens)-1):
				self.parseCommand(tokens[idx])
			data = tokens[len(tokens)-1]
			if 3==self.counting:
				break
				
	def gotAUTH(self, tokens):
		self.gotAuth = True
	
	def parseCommand(self, commandLine):
		tokens = commandLine.split()
		command = tokens[0]
		try:
			method = self.__getattribute__("got"+command)
			method(tokens)
		except AttributeError:
			pass
			
	def testReceive(self):
		self.gotAuth = False
		self.parseReceiveData()
		self.assertTrue(self.gotAuth)
		
if __name__ == '__main__':
    unittest.main()