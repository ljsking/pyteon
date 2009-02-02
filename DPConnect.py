from BaseConnect import *
import md5
		
class DPConnect(BaseConnect):
	def __init__(self, id, password, ip, port):
		super(DPConnect, self).__init__(ip, port)
		self.id = id
		self.password = password
		
	def connect(self):
		super(DPConnect, self).connect()
		self.send('LSIN', "%s %s MD5 3.871 UTF8\r\n"%(self.id, self.digest()))
		
	def digest(self):
		m = md5.new()
		m.update(self.password)
		m.update(self.id)
		digest = m.digest()
		data = ''
		for a in digest:
			data += '%02x'%ord(a)
		return data
		
	def gotLSIN(self, data):
		self.send('CONF', '0 0\r\n')
		
	def gotCONF(self, data):
		tokens = data.split()
		prefixsize = data.find('\r\n')+2
		originalSize = int(tokens[3])+prefixsize
		receivedSize = len(data)
		while originalSize > receivedSize:
			data = self.socket.recv(1024)
			receivedSize += len(data)
			#print "%d/%d\n"%(receivedSize, originalSize)
			
		self.send('GLST', '3 0\r\n')
		
	def gotGLST(self, data):
		print 'got GLST'
