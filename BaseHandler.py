import asyncore, socket
class BaseHandler(object):
	def __init__(self, host, port, client):
		asyncore.dispatcher.__init__(self)
		self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
		self.buffer = ''
		self.host = host
		self.port = port
		self.seq = 0
		
	def writable(self):
		return (len(self.buffer) > 0)
		
	def connectToServer(self):
		self.connect( (self.host, self.port) )
	
	def send(self, command, arg):
		self.buffer = '%s %d %s'%(command, self.seq, arg)
		self.seq += 1
		
	def handle_close(self):
		self.close()
	
	def handle_write(self):
		sent = self.send(self.buffer)
		self.buffer = self.buffer[sent:]
		
	def handle_read(self):
		print 'handle_read'
	   	data = self.recv(8192)
		command = data[:data.find(" ")]
		try:
			method = self.__getattribute__("got"+command)
			method(data)
		except AttributeError:
			print data
		
		
