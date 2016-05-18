import random, sys, time, subprocess

from enum import Enum

class custom_triggers(Enum):
	OVERHEAT = 1024;

class module():

	provides = "temp";

	version = "0.0.1";
	
	def overheat_checker(self, event):
		while True:
			time.sleep(8);
			if max(self.get_temp()) > 70:
				event(self, custom_triggers.OVERHEAT);

	listeners = [overheat_checker];

	def trigger_10_called(self, send_request):
		send_request(["OVERHEAT WARNING", self.get_value()])

	def __init__(self, register, triggers):
		register(self, custom_triggers.OVERHEAT, self.trigger_10_called);
		register(self, triggers.STARTUP);

	def get_temp(self):
		lines = subprocess.check_output(["sensors"]).decode("utf-8").split("\n")
		result = []
		for line in lines:
			for word in line.split(" "):
				if '°' in word:
					result.append(float(word[:-2]))
					break # only get the first one from each line
		return result

	def server_request(self, server_request = None):
		return self.get_temp();

	def trigger_called(self, trigger):
		return self.get_temp();
