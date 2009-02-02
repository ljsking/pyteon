from BaseConnect import *

class DPLConnect(BaseConnect):
	def __init__(self, id, connected):
		super(DPLConnect, self).__init__('dpl.nate.com', 5004)
		self.id = id
		self.connected = connected
		
	def connect(self):
		super(DPLConnect, self).connect()
		self.send('PVER', '3.871 3.0 ko.linux\r\n')
			
	def gotPVER(self, data):
		self.send('AUTH', 'AUTH\r\n')
		
	def gotAUTH(self, data):
		self.send('REQS', 'DES %s\r\n'%(self.id))
		
	def gotREQS(self, data):
		tokens = data.split()
		self.connected(tokens[3], int(tokens[4]))
		