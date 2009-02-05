import asynchat, asyncore
import logging, md5
from socket import *

logging.basicConfig(level=logging.DEBUG, format="%(created)-15s %(levelname)8s %(thread)d %(name)s %(message)s")
log						= logging.getLogger(__name__)

class BaseHandler(asynchat.async_chat):
	
	LINE_TERMINATOR		= "\r\n"
	
	def __init__(self, conn_sock):
		asynchat.async_chat.__init__(self, conn_sock)
		self.ibuffer			= []
		self.set_terminator(self.LINE_TERMINATOR)
	
	def collect_incoming_data(self, data):
		self.ibuffer.append(data)
	
	def send_data(self, data):
		log.debug("sending: [%s]" % data)
		self.push(data+self.LINE_TERMINATOR)

	def handle_close(self):
		log.info("conn_closed")
		asynchat.async_chat.handle_close(self)
		
class DPLHandler(BaseHandler):
	def __init__(self, conn_sock):
		BaseHandler.__init__(self, conn_sock)
		self.send_data('PVER 0 3.871 3.0 ko.linux')
		
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
		self.send_data('AUTH 1 AUTH')
		
	def gotAUTH(self):
		log.debug("call gotAUTH")
		self.send_data('REQS 2 DES ljsking@netsgo.com')
		
	def gotREQS(self):
		log.debug("call gotREQS")
		tokens = self.ibuffer[0].split()
		log.debug(tokens)
		host = tokens[3]
		port = int(tokens[4])
		
		s = socket(AF_INET, SOCK_STREAM)
		s.connect((host, port))
		handler = DPHandler(s)

class DPHandler(BaseHandler):

	LINE_TERMINATOR		= "\r\n"

	def __init__(self, conn_sock):
		BaseHandler.__init__(self, conn_sock)
		self.handler = ''
		self.send_data('LSIN 0 %s %s MD5 3.871 UTF8'%('ljsking@netsgo.com', self.digest()))
		
	def digest(self):
		m = md5.new()
		m.update('rjseka')
		m.update('ljsking@netsgo.com')
		digest = m.digest()
		data = ''
		for a in digest:
			data += '%02x'%ord(a)
		return data
		
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

		
class Runner(object):
	def __init__(self):
		s = socket(AF_INET, SOCK_STREAM)
		s.connect(('dpl.nate.com', 5004))
		dplHandler = DPLHandler(s)
		
		#c=Connection(DPLHandler)
		#c.connectToServer('dpl.nate.com', 5004)
		#c.sendCommand('PVER', '3.871 3.0 ko.linux\r\n')
		asyncore.loop()

runner = Runner()