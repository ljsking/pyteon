from socket import *
import md5
class Connect(object):
	def __init__(self, id, password):
		self.id = id
		self.password = password
	def connectToDPL(self):
		dplHost = 'dpl.nate.com'
		dplPort = 5004
		self.dplSocket = socket(AF_INET, SOCK_STREAM)
		self.dplSocket.connect((dplHost, dplPort))
		self.dplSocket.send('PVER 1 3.871 3.0 ko.linux\r\n')
		if self.dplSocket.recv(1024).split()[0] != 'PVER':
			raise Exception('Cant get a PVER')
		self.dplSocket.send('AUTH 2 AUTH\r\n') 
		if self.dplSocket.recv(1024).split()[0] != 'AUTH':
			raise Exception('Cant get a AUTH')
		self.dplSocket.send('REQS 3 DES '+self.id+'\r\n') 
		tokens = self.dplSocket.recv(1024).split()
		self.dpHost = tokens[3]
		self.dpPort = int(tokens[4])
	def connectToDP(self):
		m = md5.new()
		m.update(self.password)
		m.update(self.id)
		digest = m.digest()
		data = ''
		for a in digest:
			data += '%02x'%ord(a)
		
		self.dpSocket = socket(AF_INET, SOCK_STREAM)
		self.dpSocket.connect((self.dpHost, self.dpPort))
		data = "%s %s MD5 3.871 UTF8"%(self.id, data)
		self.dpSocket.send('LSIN 1 %s\r\n'%data)
		print self.dpSocket.recv(1024)