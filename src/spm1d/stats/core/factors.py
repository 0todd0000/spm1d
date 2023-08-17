
import itertools
import numpy as np


class Factor(object):
	def __init__(self, A, name='A', name_s=None, level_names=None):
		self.A            = np.asarray(A, dtype=int)        #integer vector of factor levels
		self.J            = None     # number of observations
		self.u            = None     # unique levels
		self.n            = None     # number of levels
		self.name         = None     # factor label
		self.name_s       = None     # factor label short (for summary table display)
		self.unames       = None     # factor level labels
		# self.isnested     = False    # nested flag
		# self.nested       = None
		# self.balanced     = True
		self.set_name(name, name_s)
		self._parse( level_names )



	def __repr__(self):
		s  = f'Factor "{self.name}"\n'
		s += f'    name        = {self.name}\n'
		s += f'    name_s      = {self.name_s}\n'
		s += f'    J           = {self.J}\n'
		s += f'    n           = {self.n}\n'
		s += f'    u           = {self.u}\n'
		s += f'    unames      = {self.unames}\n'
		return s
	
	def _parse(self, level_names):
		self.J            = self.A.size
		self.u            = np.unique(self.A)
		self.n            = self.u.size
		if level_names is None:
			self.unames   = [f'{self.name}{uu}'  for uu in self.u]
		else:
			self.unames   = [str(s) for s in level_names]
		

	@property
	def level_names(self):
		return self.unames
	@property
	def nlevels(self):
		return self.n

	def get_design_interaction(self, other):
		XAB        = []
		A,B        = self.A, other.A
		for uB in other.u[1:]:
			for uA in self.u[1:]:
				x      = np.zeros(self.J)
				x[(A==uA)&(B==uB)] =  1
				XAB.append(x)
		return np.array(XAB).T

	def get_design_intercept(self):
		return np.ones((self.J,1))
	
	def get_design_main(self):
		X = []
		for u in self.u:
			x = np.zeros(self.J)
			x[self.A==u] =  1
			X.append(x)
		return np.array( X ).T

	# def get_design_mway_main(self):
	# 	X = []
	# 	for i,u0 in enumerate(self.u[:-1]):
	# 		for u1 in self.u[i+1:]:
	# 			x = np.zeros(self.J)
	# 			x[self.A==u0] = -1
	# 			x[self.A==u1] = +1
	# 			X.append(x)
	# 	return np.array( X ).T

	def get_design_mway_main(self):
		X = []
		for i,u0 in enumerate(self.u[:-1]):
			x = np.zeros(self.J)
			x[self.A==u0] = 1
			x[self.A==self.u[-1]] = -1
			X.append(x)
			# for u1 in self.u[i+1:]:
			#
			# 	x[self.A==u0] = -1
			# 	x[self.A==u1] = +1
			#
		return np.array( X ).T
		
		
	def get_design_mway_interaction(self, other):
		A,B  = self.A, other.A
		XAB  = []
		for uA0,uA1 in itertools.combinations(self.u, 2):
			for uB0,uB1 in itertools.combinations(other.u, 2):
				x      = np.zeros(self.J)
				x[(A==uA0)&(B==uB0)] =  +1
				x[(A==uA0)&(B==uB1)] =  -1
				x[(A==uA1)&(B==uB0)] =  -1
				x[(A==uA1)&(B==uB1)] =  +1
				XAB.append(x)
		return np.array(XAB).T
		
		
	def set_name(self, name, name_s=None):
		self.name   = str(name).upper()
		self.name_s = self.name if (name_s is None) else str(name_s).upper()

	