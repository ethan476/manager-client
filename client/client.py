import logging, time, sys, glob, threading, queue;

from .triggers import Triggers;

class Client():

	def event(self, module, server_request):
		for q in listener_queues:
			q.put([module.provides, server_request]);

	def listener(self, q, trigger, p, module, trigger_done):
		while True:
			temp = q.get();
			if temp == [module.provides, trigger]:
				p.put([module.provides, trigger_done(trigger)]);
			elif temp[0] == module:
				p.put([module.provides, module.get_value(temp[1])]);

	def global_queue_listener_function(self, p):
		while True:
			self.server_send(p.get());

	def register(self, module, trigger, trigger_done=False):
		if not trigger_done:
			trigger_done = module.trigger_called
		q = queue.Queue()
		h = threading.Thread(target = self.listener, args = (q, trigger, global_event_queue, module, trigger_done));
		h.start();
		listeners.append(h);
		listener_queues.append(q);

	def __init__(self):
		logging.info('Started Client();');

		self.global_event_queue = queue.Queue();

		sys.path.append("modules");
		modules = [g.module(self.register, Triggers) for g in map(__import__, [f[len("modules") + 1:] for f in glob.glob("modules/*")])]
		global_queue_listener = threading.Thread(target = self.global_queue_listener_function, args = (self.global_event_queue,))
		global_queue_listener.start()
		for module in modules:
			self.event(module, Triggers.STARTUP)
			for thread in module.listeners:
				h = threading.Thread(target = thread, args = (self.event,))
				h.start()
		while True:
			time.sleep(10);

	def server_send(self, data): 
		pass