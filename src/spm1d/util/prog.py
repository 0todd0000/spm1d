
'''
Progress bar
'''

import sys

class ProgressBar(object):
	'''
	A progress bar for reporting simulation progress to the terminal.
	
	Thank you ChristopheD!!
	http://stackoverflow.com/questions/3160699/python-progress-bar#3160819
	
	This implementation of ProgressBar was copied from power1d
	https://github.com/0todd0000/power1d
	'''
	def __init__(self, width=50, iterations=100):
		sys.stdout.write("[Simulating%s]" % (" " * width))
		sys.stdout.flush()
		sys.stdout.write("\b" * (width+1)) # return to start of line, after '['
		self.update_interval  = float(iterations) / width
		self.i0               = -self.update_interval
	def destroy(self):
		sys.stdout.write("\n\n")
	def update(self, i):
		if (i -self.i0) > self.update_interval:
			sys.stdout.write(".")
			sys.stdout.flush()
			self.i0          += self.update_interval
			
			
class NullProgressBar(object):
	'''
	A progress bar that does nothing.
	
	This is a convenience class to simply toggling on and off an actual progress bar.
	'''
	def destroy(self):
		pass
	def update(self, i):
		pass
