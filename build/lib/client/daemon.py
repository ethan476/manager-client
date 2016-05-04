import sys, os, time, logging, atexit;

from signal import SIGTERM;

class Daemon():
	def __init__(self, runnable, pidfile = '/tmp/pidfile', stdin = '/dev/null', stdout = '/dev/null', stderr = '/tmp/stderr'):
		self.stdin = stdin;
		self.stdout = stdout;
		self.stderr = stderr;
		self.runnable = runnable;
		self.pidfile = pidfile;

	def daemonize(self):
		logging.info('Attempting to daemonize process.');
		try:
			pid = os.fork();
			if pid > 0:
				sys.exit(0);
		except OSError as e:
			logging.error("fork #1 failed: %d (%s)\n" % (e.errno, e.strerror));
			sys.exit(1);

		#os.chdir("/");
		os.setsid();
		os.umask(0);

		try:
			pid = os.fork();
			if pid > 0:
				sys.exit(0);
		except OSError as e:
			logging.error("fork #2 failed: %d (%s)\n" % (e.errno, e.strerror));
			sys.exit(1);

		sys.stdout.flush();
		sys.stderr.flush();
		si = open(self.stdin, 'rb');
		so = open(self.stdout, 'ab+');
		se = open(self.stderr, 'ab+', 0);
		os.dup2(si.fileno(), sys.stdin.fileno());
		os.dup2(so.fileno(), sys.stdout.fileno());
		os.dup2(se.fileno(), sys.stderr.fileno());

		atexit.register(self.delpid);
		pid = str(os.getpid());
		open(self.pidfile, 'w+').write("%s\n" % pid);

		logging.info('Daemonized process with pid %s.', pid);


	def delpid(self):
		os.remove(self.pidfile);

	def getpid(self):
		try:
			pf = open(self.pidfile, 'r');
			pid = int(pf.read().strip());
			pf.close();
		except IOError:
			pid = None;

			if os.path.exists(self.pidfile):
				os.remove(self.pidfile);

		return pid;


	def start(self):
		logging.info('Attempting to start service.');
		
		if self.running():
			logging.warning('Failed to start, service is already running.');
			return False;

		self.daemonize();
		self.run();

	def stop(self):
		logging.info('Attempting to stop service.');

		try:
			pf = open(self.pidfile, 'r');
			pid = int(pf.read().strip());
			pf.close();
		except IOError:
			pid = None;

			if os.path.exists(self.pidfile):
				os.remove(self.pidfile);

		if pid:
			try:
				while 1:
					os.kill(pid, SIGTERM);
					time.sleep(0.1);
			except OSError as err:
				err = str(err);
				if err.find("No such process") > 0:
					if os.path.exists(self.pidfile):
						os.remove(self.pidfile);
				else:
					logging.error(err);
					sys.exit(1);

		logging.info('Service stopped.');


	def restart(self):
		logging.info('Attempting to restart service.');
		self.stop();
		self.start();

	def running(self):
		pid = self.getpid();

		if pid:
			try:
				os.kill(pid, 0);
			except OSError:
				return False;
			else:
				return True;

		return False;

	def run(self):
		logging.info('Executing runnable.');
		self.runnable();