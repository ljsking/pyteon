import asynchat, asyncore, socket
import logging, md5

logging.basicConfig(level=logging.DEBUG, format="%(created)-15s %(levelname)8s %(thread)d %(name)s %(message)s")
log						= logging.getLogger(__name__)

class Connection(asyncore.dispatcher):
	def __init__(self, handlerClass):
		asyncore.dispatcher.__init__(self)
		self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
		self.seq = 0
		self.handlerClass = handlerClass
	
	def connectToServer(self, host, port):
		self.connect( (host, port) )

	def handle_connect(self):
		pass

	def handle_close(self):
		self.close()
		print "closed"

	def handle_read(self):
		self.handlerClass(self)

	def writable(self):
		return (len(self.sendBuffer) > 0)

	def handle_write(self):
		sent = self.send(self.sendBuffer)
		self.sendBuffer = self.sendBuffer[sent:]

	def sendCommand(self, command, arg):
		self.sendBuffer = '%s %d %s'%(command, self.seq, arg)
		self.seq += 1
		
class DPLHandler(asynchat.async_chat):
	
	LINE_TERMINATOR		= "\r\n"
	
	def __init__(self, conn_sock):
		asynchat.async_chat.__init__(self, conn_sock)
		self.ibuffer			= []
		self.set_terminator(self.LINE_TERMINATOR)

	
	def collect_incoming_data(self, data):
		log.debug("collect_incoming_data: [%s]" % data)
		self.ibuffer.append(data)

	
	def found_terminator(self):
		log.debug("found_terminator")
		line = self.ibuffer[0]
		command = line.split()[0]
		log.debug("command is " + command)
		method = 'got' + command
		if hasattr(self,method):
			getattr(self,method)()
		self.ibuffer = self.ibuffer[1:]
			
	def gotPVER(self):
		log.debug("call gotPVER")
		#self.sendCommand('AUTH', 'AUTH\r\n')
		self.send_data('AUTH 1 AUTH')
		#self.ibuffer = []
		
	def gotAUTH(self):
		log.debug("call gotAUTH")
		#self.sendCommand('AUTH', 'AUTH\r\n')
		self.send_data('REQS 2 DES ljsking@netsgo.com')
		#self.ibuffer = []
		
	def gotREQS(self):
		log.debug("call gotREQS")
		tokens = self.ibuffer[0].split()
		log.debug(tokens)
		host = tokens[3]
		port = int(tokens[4])
		c=Connection(DPHandler)
		c.connectToServer(host, port)
		c.sendCommand('LSIN', '%s %s MD5 3.871 UTF8\r\n'%('ljsking@netsgo.com', self.digest()))

	def digest(self):
		m = md5.new()
		m.update('rjseka')
		m.update('ljsking@netsgo.com')
		digest = m.digest()
		data = ''
		for a in digest:
			data += '%02x'%ord(a)
		return data
		
	def send_data(self, data):
		log.debug("sending: [%s]" % data)
		self.push(data+self.LINE_TERMINATOR)
	
	def handle_close(self):
		log.info("conn_closed")
		#asynchat.async_chat.handle_close(self)

class DPHandler(asynchat.async_chat):

	LINE_TERMINATOR		= "\r\n"

	def __init__(self, conn_sock):
		asynchat.async_chat.__init__(self, conn_sock)
		self.ibuffer			= []
		self.set_terminator(self.LINE_TERMINATOR)
		self.handler = ''

	def collect_incoming_data(self, data):
		#log.debug("collect_incoming_data: [%s]" % data)
		self.ibuffer.append(data)

	def found_terminator(self):
		if self.handler != '':
			log.debug("found_terminator with handler")
			method = self.handler
			self.handler = ''
			data = ''.join(self.ibuffer)
			self.set_terminator(self.LINE_TERMINATOR)
			self.ibuffer = []
		else:
			log.debug("found_terminator")
			data = self.ibuffer[0]
			self.ibuffer=self.ibuffer[1:]
			command = data[:data.find(" ")]
			method = 'got' + command
			if command == 'CONF':
				self.handler = 'got'+command
				tokens = data.split()
				self.set_terminator(int(tokens[3]))
		
		if self.handler == '':
			if hasattr(self,method):
				getattr(self,method)(data)
			else:
				log.debug("No has attribute: %s" % method)
			
	def gotLSIN(self, data):
		log.debug('gotLSIN')
		self.send_data('CONF 1 0 0')
		
	def gotCONF(self, data):
		log.debug("gotCONF with ")
		log.debug(unicode(data,'utf-8'))

	def send_data(self, data):
		log.debug("sending: [%s]" % data)
		self.push(data+self.LINE_TERMINATOR)

	def handle_close(self):
		log.info("conn_closed")
		#asynchat.async_chat.handle_close(self)
class Runner(object):
	def __init__(self):
		c=Connection(DPLHandler)
		c.connectToServer('dpl.nate.com', 5004)
		c.sendCommand('PVER', '3.871 3.0 ko.linux\r\n')
		asyncore.loop()

runner = Runner()