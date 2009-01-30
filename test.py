import unittest
from connect import *
class TestSequenceFunctions(unittest.TestCase):
	def setUp(self):
		self.con = Connect('ljsking@netsgo.com','rjseka')

	def testConnectToDPL(self):
		self.con.connectToDPL()
		self.assertTrue(self.con.dpHost!=None)
		self.assertTrue(self.con.dpPort!=None)
		
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
		self.con.connectToDPL()
		self.con.connectToDP()
		
if __name__ == '__main__':
    unittest.main()

#sendCommand( "PVER", "" )