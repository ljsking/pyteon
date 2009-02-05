#!/usr/bin/env python
# encoding: utf-8
from BaseHandler import *
from Buddy import *
import md5
import logging

log						= logging.getLogger(__name__)

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