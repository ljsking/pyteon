import asynchat
import logging

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