from nose.tools import *
import fehBrowse
from fehBrowse.stderr import eprint

def setup():
	print("SETUP!")

def teardown():
	print("TEAR DOWN!")

def test_basic():
	print("I RAN!")

def test_eprint():
	eprint("This is going to the standard error stream.")

