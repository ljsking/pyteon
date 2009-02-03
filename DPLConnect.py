from BaseConnect import *
from DPConnect import *

class DPLConnect(BaseConnect):
	def __init__(self, client):
		super(DPLConnect, self).__init__('dpl.nate.com', 5004, client)
		
	def connect(self):
		super(DPLConnect, self).connect()
		self.send('PVER', '3.871 3.0 ko.linux\r\n')
			
	def gotPVER(self, data):
		self.send('AUTH', 'AUTH\r\n')
		
	def gotAUTH(self, data):
		self.send('REQS', 'DES %s\r\n'%(self.client.id))
		
	def gotREQS(self, data):
		tokens = data.split()
		ip = tokens[3]
		port = int(tokens[4])
		self.client.dpConnect = DPConnect(ip, port, self.client)
		self.client.dpConnect.connect()