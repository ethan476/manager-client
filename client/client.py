import logging, time, sys, glob;

from triggers import Triggers;

class Client():

	def event(module, server_request):
		for q in listener_queues:
			q.put([module.provides, server_request]);

	def listener(q, trigger, p, module):
		while True:
			temp = q.get();
			if temp == [module.provides, trigger]:
				p.put([module.provides, module.trigger_called(trigger)]);
			elif temp[0] == module:
				p.put([module.provides, module.get_value(temp[1])]);

	def global_queue_listener_function(p):
		while True:
			server_send(p.get());

	def register(module, trigger):
		q = queue.Queue()
		h = threading.Thread(target = listener, args = (q, trigger, global_event_queue, module));
		h.start();
		listeners.append(h);
		listener_queues.append(q);

	def __init__(self):
		logging.info('Started Client();');

		sys.path.append("modules");
		modules = [g.module(register, Triggers) for g in map(__import__, [f[len("modules") + 1:] for f in glob.glob("modules/*")])]
		global_queue_listener = threading.Thread(target = global_queue_listener_function, args = (global_event_queue,))
		global_queue_listener.start()
		for module in modules:
			event(module, Triggers.STARTUP)
			for thread in module.listeners:
				h = threading.Thread(target = thread, args = (event,))
				h.start()
		while True:
			time.sleep(10);
