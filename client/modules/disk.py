import subprocess

class module():

	provides = "disk";

	version = "0.0.1";
	
	listeners = [];

	def __init__(self, register, triggers):
		self.triggers = triggers
		register(self, triggers.STARTUP);
		register(self, triggers.USER);
		register(self, triggers.SHUTDOWN);

	def get_value(self):
		lines = subprocess.check_output(["df"]).decode("utf-8").split("\n")
		for line in lines:
			if line[-1] == "/":
				return [int(line.split()[2])/1024.0/1024, int(line.split()[1])/1024.0/1024]

	def server_request(self, server_request = None):
		return self.get_value();

	def trigger_called(self, trigger):
		if trigger == self.triggers.STARTUP:
			print("CPU module ready")
		elif trigger == self.triggers.SHUTDOWN:
			# close file descriptors or some shit
			print("CPU module cleaned up and shut down sucessfully")
		return self.get_value();
