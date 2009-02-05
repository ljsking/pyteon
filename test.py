import asynchat, asyncore
import logging, md5
from socket import *
from MockClient import *
from Buddy import *

logging.basicConfig(level=logging.DEBUG, format="%(created)-15s %(levelname)8s %(thread)d %(name)s %(message)s")
log						= logging.getLogger(__name__)

class BaseHandler(asynchat.async_chat):
	
	LINE_TERMINATOR		= "\r\n"
	
	def __init__(self, conn_sock, client):
		asynchat.async_chat.__init__(self, conn_sock)
		self.ibuffer			= ""
		self.set_terminator(self.LINE_TERMINATOR)
		self.count = 0
		self.client = client
		
	
	def collect_incoming_data(self, data):
		self.ibuffer = self.ibuffer + data
	
	def send_data(self, command, data):
		log.debug("sending: [%s]" % data)
		self.push('%s %d %s%s'%(command, self.count, data, self.LINE_TERMINATOR))
		self.count+=1
		
	def handle_close(self):
		log.info("conn_closed")
		asynchat.async_chat.handle_close(self)
		
class DPLHandler(BaseHandler):
	def __init__(self, conn_sock, client):
		BaseHandler.__init__(self, conn_sock, client)
		self.send_data('PVER', '3.871 3.0 ko.linux')
		
	def found_terminator(self):
		#log.debug("found_terminator")
		print self.ibuffer
		data = self.ibuffer
		self.ibuffer = ''
		command = data[:data.find(" ")]
		log.debug("command is " + command)
		method = 'got' + command
		if hasattr(self,method):
			getattr(self,method)(data)
		
	def gotPVER(self, data):
		log.debug("call gotPVER")
		self.send_data('AUTH', 'AUTH')
		
	def gotAUTH(self, data):
		log.debug("call gotAUTH")
		self.send_data('REQS', 'DES %s'%self.client.id)
		
	def gotREQS(self, data):
		log.debug("call gotREQS")
		
		tokens = data.split()
		host = tokens[3]
		port = int(tokens[4])
		s = socket(AF_INET, SOCK_STREAM)
		s.connect((host, port))
		handler = DPHandler(s, self.client)

class DPHandler(BaseHandler):

	LINE_TERMINATOR		= "\r\n"

	def __init__(self, conn_sock, client):
		BaseHandler.__init__(self, conn_sock, client)
		self.handler = ''
		self.send_data('LSIN', '%s %s MD5 3.871 UTF8'%(self.client.id, self.digest()))
		
		
	def digest(self):
		m = md5.new()
		m.update(self.client.password)
		m.update(self.client.id)
		digest = m.digest()
		data = ''
		for a in digest:
			data += '%02x'%ord(a)
		return data
		
	def found_terminator(self):
		#print unicode(self.ibuffer,'utf-8')
		if self.handler != '':
			method = self.handler
			self.handler = ''
			data = self.ibuffer
			self.set_terminator(self.LINE_TERMINATOR)
			self.ibuffer = ''
		else:
			data = self.ibuffer
			self.ibuffer=""
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
		self.send_data('CONF', '0 0')
		
	def gotCONF(self, data):
		log.debug("gotCONF with ")
		self.send_data('GLST', '3 0')
		
	def gotGLST(self, data):
		tokens = data.split()
		if 7 == len(tokens):
			if tokens[4] == 'Y':
				groupName=unicode(tokens[6],'utf-8')
				id = int(tokens[5])
				self.client.groups[id]=groupName
			start = int(tokens[2])
			end = int(tokens[3])
			if start+1 == end:
				self.send_data('LIST', '')
				
	def gotLIST(self, data):
		tokens = data.split()
		#logging.debug('%s'%unicode(data,'utf-8'))
		if 19 == len(tokens):
			groupID = int(tokens[4])
			email = tokens[5]
			name = unicode(tokens[7],'utf-8')
			nick = unicode(tokens[8],'utf-8')
			
			id = int(tokens[6])
			self.client.buddies[id]=Buddy(name,nick,email,groupID)
			start = int(tokens[2])
			end = int(tokens[3])
		
class Runner(object):
	def __init__(self):
		s = socket(AF_INET, SOCK_STREAM)
		s.connect(('dpl.nate.com', 5004))
		dplHandler = DPLHandler(s, MockClient())
		asyncore.loop()

runner = Runner()