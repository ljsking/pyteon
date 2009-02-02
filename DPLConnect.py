from socket import *
class DPLConnect(object):
	dplHost = 'dpl.nate.com'
	dplPort = 5004
	def __init__(self, id, connected):
		self.seq = 0
		self.id = id
		self.connected = connected
	def connect(self):
		self.socket = socket(AF_INET, SOCK_STREAM)
		self.socket.connect((self.dplHost, self.dplPort))
		self.send('PVER', '3.871 3.0 ko.linux\r\n')
		
	def send(self, command, arg):
		self.socket.send('%s %d %s'%(command, self.seq, arg))
		self.seq += 1
		self.receive()
		
	def receive(self):
		data = ''
		self.counting = 0
		data += self.socket.recv(1024)
		tokens = data.split('\r\n')
		for idx in range(0, len(tokens)-1):
			self.parseCommandLine(tokens[idx])
		data = tokens[len(tokens)-1]
		
	def parseCommandLine(self, commandLine):
		tokens = commandLine.split()
		command = tokens[0]
		try:
			method = self.__getattribute__("got"+command)
			method(tokens)
		except AttributeError:
			print commandLine
			
	def gotPVER(self, tokens):
		self.send('AUTH', 'AUTH\r\n')
		
	def gotAUTH(self, tokens):
		self.send('REQS', 'DES %s\r\n'%(self.id))
		
	def gotREQS(self, tokens):
		self.connected(tokens[3], int(tokens[4]))
		