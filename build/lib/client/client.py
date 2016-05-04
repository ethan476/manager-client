import logging, time, sys, glob, threading, queue, os

from .triggers import Triggers;

class Client():

	def event(self, module, server_request, trigger = True):
		for q in self.listener_queues:
			q.put([module, server_request, trigger]);

	def listener(self, q, trigger, p, module, trigger_done):
		while True:
			temp = q.get();
			if temp == [module.provides, trigger, True]:
				p.put([module, True, trigger_done(trigger)]);
	def server_request_listener(self, q, p, module):
		while True:
			temp = q.get();
			if temp[0] == module.provides and not temp[2]:
				p.put([module, False, module.get_value(temp[1])])
	def global_queue_listener_function(self, p):
		while True:
			self.server_send(*p.get());

	def register(self, module, trigger, trigger_done = False, server_request = False):
		if not trigger_done:
			trigger_done = module.trigger_called
		q = queue.Queue()
		if server_request:
			h = threading.Thread(target = self.server_request_listener, args = (q, self.global_event_queue, module));
		else:
			h = threading.Thread(target = self.listener, args = (q, trigger, self.global_event_queue, module, trigger_done));
		self.listeners.append(h);
		self.listener_queues.append(q);
		h.start();

	def __init__(self):
		logging.info('Started Client();');

		self.global_event_queue = queue.Queue();
		self.listeners = []
		self.listener_queues = []
		sys.path.append("client/modules");
		old_files = [f[len("client/modules") + 1:] for f in glob.glob("client/modules/*")]
		files = []
		for f in old_files:
			if f != "__pycache__":
				files.append(f[:-3])
		modules = [g.module(self.register, Triggers) for g in map(__import__, files)]
		global_queue_listener = threading.Thread(target = self.global_queue_listener_function, args = (self.global_event_queue,))
		global_queue_listener.start()
		for module in modules:
			self.event(module, Triggers.STARTUP)
			self.register(module, False, False, True)
			for thread in module.listeners:
				h = threading.Thread(target = thread, args = (module, self.event,))
				h.start()


		time.sleep(1);
		self.event("temp", 'This is a test', False);

		while True:
			time.sleep(10);


	def prepare_packet(self):
		pass

	def server_send(self, module, was_trigger, data): 
		print(module, was_trigger, data)