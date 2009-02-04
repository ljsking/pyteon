#!/usr/bin/env python
# encoding: utf-8
from BaseConnect import *
from Buddy import *
import md5
		
class DPConnect(BaseConnect):
	def __init__(self, ip, port, client):
		super(DPConnect, self).__init__(ip, port, client)
		
	def connect(self):
		super(DPConnect, self).connect()
		self.send('LSIN', "%s %s MD5 3.871 UTF8\r\n"%(self.client.id, self.digest()))
		
	def digest(self):
		m = md5.new()
		m.update(self.client.password)
		m.update(self.client.id)
		digest = m.digest()
		data = ''
		for a in digest:
			data += '%02x'%ord(a)
		return data
		
	def gotLSIN(self, data):
		self.send('CONF', '0 0\r\n')
		
	def gotCONF(self, data):
		tokens = data.split()
		prefixsize = data.find('\r\n')+2
		originalSize = int(tokens[3])+prefixsize
		receivedSize = len(data)
		while originalSize > receivedSize:
			data = self.socket.recv(1024)
			receivedSize += len(data)
		self.send('GLST', '3 0\r\n')
		
	def gotGLST(self, data):
		lines = data.split('\r\n')
		tokens = lines[0].split()
		lines = lines[1:]
		groupSize = int(tokens[2])
		done = False
		while not done:
			for line in lines[:-1]:
				tokens = line.split()
				if tokens[4] == 'Y':
					gourpName=unicode(tokens[6],'utf-8')
					id = int(tokens[5])
					self.client.groups[id]=gourpName
				start = int(tokens[2])
				end = int(tokens[3])
				done = start+1==end
				if done:
					break
			if not done:
				data =lines[-1]+self.socket.recv(1024)
			 	lines = data.split('\r\n')
		self.send('LIST', '\r\n')
		
	def gotLIST(self, data):
		lines = data.split('\r\n')
		done = False
		while not done:
			for line in lines[:-1]:
				tokens = line.split()
				groupID = int(tokens[4])
				email = tokens[5]
				name = unicode(tokens[7],'utf-8')
				nick = unicode(tokens[8],'utf-8')
				id = int(tokens[6])
				self.client.buddies[id]=Buddy(name,nick,email,groupID)
				
				start = int(tokens[2])
				end = int(tokens[3])
				done = start+1==end
				
				if done:
					break
			if not done:
				data =lines[-1]+self.socket.recv(1024)
			 	lines = data.split('\r\n')
