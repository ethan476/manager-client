import logging, time, sys, glob, threading, queue, os

from .triggers import Triggers;

class Client():

	def event(self, module, server_request, trigger = True):
		logging.info('Listener_queues length: %s', len(self.listener_queues));

		for q in self.listener_queues:
			q.put([module, server_request, trigger]);

	def listener(self, q, trigger, p, module, trigger_done, server_request):
		while True:
			temp = q.get();
			if server_request and temp[0] == module.provides and not temp[2]:
				p.put([module, False, module.server_request(temp[1])]);
			elif temp == [module.provides, trigger, True]:
				p.put([module, True, trigger_done(trigger)]);

	def global_queue_listener_function(self, p):
		while True:
			self.server_send(*p.get());

	def register(self, module, trigger, trigger_method = False, server_request = False):
		
		if not trigger_method:
			trigger_method = module.trigger_called;

		q = queue.Queue();
		h = threading.Thread(target = self.listener, args = (q, trigger, self.global_event_queue, module, trigger_method, server_request));
	
		self.listeners.append(h);
		self.listener_queues.append(q);
		
		h.start();

		#logging.info('Started thread with PID: %s', h.get_ident());


	def __init__(self):
		logging.info('Started Client();');

		self.global_event_queue = queue.Queue();
		self.listeners = []
		self.listener_queues = []
		
		sys.path.append("client/modules");
		self.socket = None;


		old_files = [f[len("client/modules") + 1:] for f in glob.glob("client/modules/*")];
		files = []
		for f in old_files:
			if f != "__pycache__":
				files.append(f[:-3]);
		
		modules = [g.module(self.register, Triggers) for g in map(__import__, files)];

		global_queue_listener = threading.Thread(target = self.global_queue_listener_function, args = (self.global_event_queue,));
		global_queue_listener.start();
		
		for module in modules:

			if len(modules) == 1:
				logging.info('Loaded 1 module.', );
			else:
				logging.info('Loaded %s modules.', modules);

			self.event(module, Triggers.STARTUP);
			self.register(module, False, False, True);

			for thread in module.listeners:
				h = threading.Thread(target = thread, args = (module, self.event,));
				h.start();


		time.sleep(1);
		self.event("temp", 'This is a test', False);

		while True:
			time.sleep(10);


	def prepare_packet(self, data):
		return data

	def server_send(self, module, was_trigger, data): 
		self.socket.write(json.dumps({
			"module": module.provides,
			"version": module.version,
			"payload": prepare_packet(data),
			"auth_token": "",
			"timestamp": subprocess.check_output(["date", '+%s']).decode("utf-8").strip()
		}))