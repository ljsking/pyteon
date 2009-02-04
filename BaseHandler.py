from Connection import *

class BaseHandler(object):
	def __init__(self, host, port, client):
		self.host = host
		self.port = port
		self.client = client
	def connected(self):
		pass