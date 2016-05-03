import os, argparse, sys, logging, time;

from .daemon import Daemon;
from .client import Client;


parser = argparse.ArgumentParser();

parser.add_argument('action');


root = '/etc/manager-client/'

def init_directories():
	if not os.path.exists(root):
		os.makedirs(root);


def init_logger():

	logging.basicConfig(
		filename = root + '/manager-client.log',
		level = logging.DEBUG,
		format = '%(asctime)s %(message)s',
		datefmt = '%m/%d/%Y %I:%M:%S %p'
	);

	logger = logging.getLogger();
	logger.setLevel(logging.DEBUG);

	
def start(args):
	daemon = Daemon(Client, root + '/manager-client.pid');

	if daemon.running():
		print('Service is already running.');
		return;

	
	print('Service starting...');
	
	if not daemon.start():
		print('Failed to start, please check the logs.', file = sys.stderr);

def stop(args):
	print('Service stopping...');
	daemon = Daemon(None, root + '/manager-client.pid');
	daemon.stop();


def restart(args):
	stop(args);
	start(args);

def status(args):
	daemon = Daemon(None, root + '/manager-client.pid');

	print(daemon.running());

	if daemon.running():
		print('Service is running.');
	else:
		print('Service is stopped.');

actions = {
	'start': start,
	'stop': stop,
	'restart': restart,
	'status': status
};

def main():
	if os.geteuid() != 0:
		print('You must be root to manage server-manager.' , file = sys.stderr);
		sys.exit(1);

	init_directories();

	init_logger();

	parsed, args = parser.parse_known_args();
	action = parsed.action;

	if action in actions:
		logging.info('CLI: Executing action subroutine for \'%s\'', action);

		actions[action](args);

	else:
		print('Invalid action \'' + action + '\'', file = sys.stderr);
		parser.print_help();
