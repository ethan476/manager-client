import random, sys;

from .module import Module;

class module(Module):
	
	def trigger_sleep_8(self, event):
		while True:
			time.sleep(8);
			event(self, 10);

	def trigger_sleep_10(self, event):
		while True:
			time.sleep(10);
			event(self, 11);

	self.provides = "temp";

	self.listeners = [trigger_sleep_8, trigger_sleep_10];

	def __init__(self, register, triggers):
		register(self, 10)
		register(self, 11)
		register(self, triggers.STARTUP)

	def get_value(self, server_request = None):
		return random.randrange(30, 40);

	def trigger_called(self, trigger):
		if trigger == 10:
			return 99
		else:
			return get_value();

