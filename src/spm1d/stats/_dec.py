




class appendSPMargs(object):
	def __init__(self, f):
		self.f = f

	def __call__(self, *args, **kwargs):
		spm = self.f(*args, **kwargs)
		# spm._set_testname( self.f.__name__ )
		spm._set_args( *args, **kwargs )
		return spm