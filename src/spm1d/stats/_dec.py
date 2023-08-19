


class appendargs(object):
	def __init__(self, f):
		self.f = f

	def __call__(self, *args, **kwargs):
		spm = self.f(*args, **kwargs)
		# spm._set_testname( self.f.__name__ )
		spm._set_args( *args, **kwargs )
		return spm
		

class checkargs(object):
	def __init__(self, fn):
		import importlib
		from . import _argchecks
		self.fn      = fn
		cname        = f'Checker{ self.fn.__name__.upper() }'
		self.Checker = getattr(_argchecks, cname)
		print( self.Checker )

	def __call__(self, *args, **kwargs):
		c = self.Checker( *args, **kwargs )
		c.check()
		return self.fn(*args, **kwargs)