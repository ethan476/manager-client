import logging, time, sys, glob, threading, queue, os, time, base64, atexit, json, configparser

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
				p.put([module, trigger, trigger_done(trigger)]);

	def global_queue_listener_function(self, p):
		while True:
			self.server_send(*p.get());

	def pinger_thread(self):
		while True:
			time.sleep(self.config["ping_timeout"])
			payload = base64.b64encode(os.urandom(12)).decode("utf-8")
			timestamp = int(time.time())
			self.socket.write({
				"message_type": 0,
				"payload": payload,
				"timestamp": timestamp
				})
			self.pings_awaiting_response_queue.put([timestamp, payload])
	def ping_collector_thread(self):
		pings_awaiting_response = []
		while True:
			if not self.recieved_pings.empty():
				recieved_ping = self.recieved_pings.get()
			if not self.pings_awaiting_response_queue.empty():
				pings_awaiting_response.append(self.pings_awaiting_response_queue.get())
			i = 0
			while i < len(pings_awaiting_response):
				if pings_awaiting_response[i][1] == recieved_ping:
					del pings_awaiting_response[i]
					break
			for ping in pings_awaiting_response:
				if int(time.time() - ping[0]) > self.config["ping_timeout"] * 2:
					# We should log something here
					self.establish_socket()
					pings_awaiting_response = []

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
		self.config = configparser.ConfigParser()
		self.config.read("/etc/manager-client/config.ini")
		self.config = self.config["Global"]
		self.global_event_queue = queue.Queue();
		self.listeners = []
		self.listener_queues = []
		self.pings_awaiting_response_queue = queue.Queue()
		self.recieved_pings = queue.Queue()
		
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
			atexit.register(self.event, module, Triggers.SHUTDOWN)

			for thread in module.listeners:
				h = threading.Thread(target = thread, args = (module, lambda x, y: self.event(x,y,True),));
				h.start();

		time.sleep(1);
		self.event("temp", 'This is a test', False);

		while True:
			time.sleep(10);

	def server_send(self, module, was_trigger, data): 
		message_object = {
			"module": module.provides,
			"version": module.version,
			"mesage_type": 3,
			"payload": data,
			"auth_token": "",
			"timestamp": int(time.time())
		}
		if was_trigger:
			message_object["message_type"] = 4
			message_object["trigger"] = was_trigger
		#self.socket.write(json.dumps(message_object));
		print(json.dumps(message_object), file=sys.stderr)
	def establish_socket(self):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server = port = 0 # TODO
		self.socket.connect(server, port)