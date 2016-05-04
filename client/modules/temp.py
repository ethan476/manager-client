import random, sys, time

from enum import Enum

class custom_triggers(Enum):
	OVERHEAT = 1024;

class module():

	provides = "temp";

	version = "0.0.1";
	
	def overheat_checker(self, event):
		while True:
			time.sleep(8);
			if self.get_value() > 50:
				event(self, custom_triggers.OVERHEAT);

	listeners = [overheat_checker];

	def trigger_10_called(self):
		return ["OVERHEAT WARNING", self.get_value()]

	def __init__(self, register, triggers):
		register(self, custom_triggers.OVERHEAT, self.trigger_10_called);
		register(self, triggers.STARTUP);

	def server_request(self, server_request = None):
		return random.randrange(30, 40);

	def trigger_called(self, trigger):
		return self.get_value();