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
		data = self.dpSocket.recv(1024)
		self.dpSocket.send('CONF 2 0 0\r\n')
		count = 1
		totalLen = 0
		#CONF 2 4481 7870
		size = 0
		while True:
			data = self.dpSocket.recv(8192)
			if count == 1:
				prefixsize = data.find('\r\n')+2
				tokens = data.split()
				#print "%s %s %d %d"%(tokens[2], tokens[3], int(tokens[3])+prefixsize, prefixsize)
				size = int(tokens[3])+prefixsize
			totalsize = len(data)
			pos = -1
			tmp = data.find('\r\n')
			while tmp!=-1:
				pos = tmp
				tmp = data.find('\r\n', pos+1)
			totalLen+=totalsize
			#print "%d %d/%d:%d\n"%(count, pos, totalsize, totalLen)
			webmemo_version=4
			count+=1
			
			if size == totalLen:
				break
		
		self.dpSocket.send('GLST 3 0\r\n')
 		'''print self.dpSocket.recv(8192)
		print "\n\n\n"
		print self.dpSocket.recv(8192)
		print "\n\n\n"
		print self.dpSocket.recv(8192)'''