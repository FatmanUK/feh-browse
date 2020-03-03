from __future__ import print_function
import sys

# debug messages to stderr
def eprint(*args, **kwargs):
	print(*args, file=sys.stderr, **kwargs)

