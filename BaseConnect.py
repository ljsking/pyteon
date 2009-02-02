from socket import *
class BaseConnect(object):
	def __init__(self, ip, port):
		self.seq = 0
		self.ip = ip
		self.port = port
		
	def connect(self):
		self.socket = socket(AF_INET, SOCK_STREAM)
		self.socket.connect((self.ip, self.port))
	
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
