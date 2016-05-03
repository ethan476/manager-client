import random, sys;

from enum import Enum

class CustomTriggers(Enum):
	OVERHEAT = 1024;

class module():

	self.provides = "temp";

	self.version = "0.0.1";

	self.listeners = [overheat_checker];
	
	def overheat_checker(self, event):
		while True:
			time.sleep(8);
			if get_value() > 50:
				event(self, CustomTriggers.OVERHEAT);

	def trigger_10_called(self):
		return ["OVERHEAT WARNING", get_value()]

	def __init__(self, register, triggers):
		register(self, CustomTriggers.OVERHEAT, trigger_10_called);
		register(self, triggers.STARTUP);

	def get_value(self, server_request = None):
		return random.randrange(30, 40);

	def trigger_called(self, trigger):
		return get_value();