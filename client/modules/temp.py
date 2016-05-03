import random, sys;

from .module import Module;
from enum import Enum

class module(Module):
	
	def overheat_checker(self, event):
		while True:
			time.sleep(8);
			if get_value() > 50:
				event(self, 10);

	def trigger_10_called(self):
		return ["OVERHEAT WARNING", get_value()]

	self.provides = "temp";

	self.listeners = [overheat_checker];

	def __init__(self, register, triggers):
		register(self, 10, trigger_10_called)
		register(self, triggers.STARTUP)

	def get_value(self, server_request = None):
		return random.randrange(30, 40);

	def trigger_called(self, trigger):
		return get_value();