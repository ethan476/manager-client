import random, sys;

from .module import Module;

class Temp(Module):
	
	self.provides = "temp";

	def __init__(self):
		pass

	def get_value(self, server_request = None):
		return random.randrange(30, 40);

	def trigger_called(self, trigger):
		return get_value();

