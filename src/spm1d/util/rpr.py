

'''
Utility classes for working with classes' __repr__ method
'''



class DisplayParams(list):
	def __init__(self, obj):
		super().__init__( [ ] )
		self.obj  = obj
		
	@property
	def keys(self):
		for k,v,sfx in self:
			if v is not None:
				yield k

	def add_default_header(self):
		self.add_header( self.obj.__class__.__name__ )
	
	def add_header(self, s):
		self.append( (s, None, None) )
		
	def add(self, key, fmt='%s', suffix=None):
		self.append( (key,fmt,suffix) )

	def asstr(self):
		s = ''
		n = max( [len(k)  for k in self.keys] )
		for k,v,sfx in self:
			if v is None:
				s += f'{k}'
			elif isinstance(v, str):
				x  = getattr(self.obj, k)
				s += f'    {k:<{n}} : {v%x}'
			elif callable(v):
				x  = getattr(self.obj, k)
				s += f'    {k:<{n}} : {v(x)}'
			s += '\n' if sfx is None else f' {sfx}\n'
		return s

# class DisplayParams(list):
# 	def __init__(self, obj):
# 		super().__init__( [ ] )
# 		self.obj  = obj
#
# 	@property
# 	def keys(self):
# 		for k,v in self:
# 			if v is not None:
# 				yield k
#
# 	def add_default_header(self):
# 		self.add_header( self.obj.__class__.__name__ )
#
# 	def add_header(self, s):
# 		self.append( (s, None) )
#
# 	def add(self, key, fmt='%s'):
# 		self.append( (key,fmt) )
#
# 	def asstr(self):
# 		s = ''
# 		n = max( [len(k)  for k in self.keys] )
# 		for k,v in self:
# 			if v is None:
# 				s += f'{k}\n'
# 			elif isinstance(v, str):
# 				x  = getattr(self.obj, k)
# 				s += f'    {k:<{n}} : {v%x}\n'
# 			elif callable(v):
# 				x  = getattr(self.obj, k)
# 				s += f'    {k:<{n}} : {v(x)}\n'
# 		return s