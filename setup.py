#!/usr/bin/env python3

import os

from codecs import open
from os import path

from setuptools import setup, find_packages, Command

base = path.abspath(path.dirname(__file__));

with open(path.join(base, 'README'), encoding='utf-8') as f:
	long_description = f.read();


class CleanCommand(Command):
    """Custom clean command to tidy up the project root."""
    user_options = [];

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        os.system('rm -vrf ./build ./dist ./*.pyc ./*.tgz ./*.egg-info');

setup(
	name	= 'manager-client',
	version	= '0.0.1',

	description	= 'A sample project',
	long_description = long_description,

	url	= 'http://example.org',

	author	= 'Ethan S',
	author_email = 'mcdasethan2@gmai.com',

	license	= 'N/A',

	classifiers	= [
		'Development Status :: 3 - Alpha',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.3',
		'Programming Language :: Python :: 3.4',
		'Programming Language :: Python :: 3.5'
	],

	keywords = '',

	packages = find_packages(exclude = [
		'contrib',
		'docs',
		'tests'
	]),

	install_requires = [

	],

	extras_require = {

	},

	entry_points = {
		'console_scripts': [
			'manager-client=client:main',
		],
	}, cmdclass={
        'clean': CleanCommand,
    }
);
