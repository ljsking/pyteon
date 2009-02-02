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
		
	def gotLSIN(self, tokens):
		self.send('CONF', '0 0\r\n')
