import random, sys;

from .module import Module;
from enum import Enum

class module(Module):
	
	def trigger_sleep_8(self, event):
		while True:
			time.sleep(8);
			event(self, 10);

	def trigger_sleep_10(self, event):
		while True:
			time.sleep(10);
			event(self, 11);

	def trigger_10_called(self):
		return 99
	def trigger_11_called(self):
		return 120

	self.provides = "temp";

	self.listeners = [trigger_sleep_8, trigger_sleep_10];

	def __init__(self, register, triggers):
		register(self, 10, trigger_10_called)
		register(self, 11, trigger_11_called)
		register(self, triggers.STARTUP)

	def get_value(self, server_request = None):
		return random.randrange(30, 40);

	def trigger_called(self, trigger):
		return get_value();