
'''
Factor classes for ANOVA.
'''

# Copyright (C) 2016  Todd Pataky



import numpy as np







class Factor(object):
	def __init__(self, A):
		self.A            = np.asarray(A, dtype=int)        #integer vector of factor levels
		self.J            = None     #number of observations
		self.u            = None     #unique levels
		self.n            = None     #number of levels
		self.isnested     = False    #nested flag
		self.nested       = None
		self.balanced     = True
		self._00_parse()
		self._01_check_unbalanced()

	def _00_parse(self):
		self.J            = self.A.size
		self.u            = np.unique(self.A)
		self.n            = self.u.size
		
	def _01_check_unbalanced(self):
		nn  = [(self.A==uu).sum()   for uu in self.u]
		self.balanced = np.all( nn==nn[0] )

	def check_balanced(self, other):
		A,B = self.A, other.A
		N   = []
		for uA in self.u:
			for uB in other.u:
				N.append( ((A==uA) & (B==uB)).sum()  )
		return np.all( N==N[0] )


	def check_balanced_nested(self, other):
		A,B   = self.A, other.A
		N     = []
		for uA,UB in zip(self.u,other.u):
			for uB in UB:
				N.append( ((A==uA) & (B==uB)).sum()  )
		return np.all( N==N[0] )


	def check_balanced_nested3(self, other, another):
		A,B,C = self.A, other.A, another.A
		N     = []
		for uA,UB,UUC in zip(self.u,other.u,another.u):
			for uB,UC in zip(UB, UUC):
				for uC in UC:
					N.append( ((A==uA) & (B==uB) & (C==uC) ).sum()  )
		return np.all( N==N[0] )


	def check_balanced_rm(self, other):
		S,A = self.A, other.A
		N   = []
		for uS in self.u:
			# UA  = np.unique(A[S==uS])  #fine for Python 2.7 but not Python 3.X
			if np.size(uS)==1:
				UA  = np.unique(  A[ S==int(uS) ]  )
			elif isinstance(uS, list):  #three-way RM ANOVA
				B   = np.array( [False]*S.size )
				for uuS in uS:
					for uuuS in uuS:
						B  = np.logical_or(B, S==uuuS)
				UA  = np.unique( A[B] )
			else:  #two-way RM ANOVA
				B   = np.array( [False]*S.size )
				for uuS in uS:
					B  = np.logical_or(B, S==uuS)
				UA  = np.unique( A[B] )
			for uA in UA:
				N.append( ((S==uS) & (A==uA)).sum()  )
		return np.all( N==N[0] )



	def get_Q(self):  #non-sphericity components
		return [np.matrix(np.diag(self.A==u), dtype=float) for u in self.u]
	
	
	def get_design_interaction(self, other):
		XAB        = []
		A,B        = self.A, other.A
		for uB in other.u[1:]:
			for uA in self.u[1:]:
				x      = np.zeros(self.J)
				x[(A==uA)&(B==uB)] =  1
				XAB.append(x)
		return np.matrix(XAB).T


	def get_design_interaction_3way(self, other, another):
		XABC       = []
		A,B,C      = self.A, other.A, another.A
		for uC in another.u[1:]:
			for uB in other.u[1:]:
				for uA in self.u[1:]:
					x      = np.zeros(self.J)
					### part one:
					x[(A==uA)&(B==uB)&(C==uC)] =  1
					XABC.append(x)
		return np.matrix(XABC).T


	def get_design_interaction_4way(self, other, another, yetanother):
		X        = []
		S,A,B,C  = self.A, other.A, another.A, yetanother.A
		for uC in yetanother.u[1:]:
			for uB in another.u[1:]:
				for uA in other.u[1:]:
					for uS in self.u[1:]:
						x      = np.zeros(self.J)
						### part one:
						x[(A==uA)&(B==uB)&(C==uC)&(S==uS)] =  1
						X.append(x)
		return np.matrix(X).T



	def get_design_main(self):
		X = []
		for u in self.u[1:]:
			x        = np.zeros(self.J)
			x[self.A==u] =  1
			X.append(x)
		return np.matrix( X ).T


	def get_design_main_nested(self, other):
		A,S  = other.A, self.A
		X    = []
		for uA in other.u:
			uS = np.unique(S[A==uA])
			for u in uS[1:]:
				x        = np.zeros(self.J)
				x[(A==uA) & (S==u)] =  1
				X.append(x)
		return np.matrix( X ).T
		
		
	def get_design_interaction_nested(self, other, another):
		A,B,S  = another.A, other.A, self.A
		XAB        = []
		for uA in np.unique(A):
			uS = np.unique(S[A==uA])
			
			for uB in other.u[1:]:
				for u in uS[1:]:
					x      = np.zeros(self.J)
					x[(A==uA)&(B==uB)&(S==u)] =  1
					XAB.append(x)
		return np.matrix(XAB).T
	





class FactorNested(Factor):
	def __init__(self, A, nestfactor):
		self.NEST       = nestfactor
		super(FactorNested, self).__init__(A)


	def _00_parse(self):
		self.J          = self.A.size
		self.u          = [np.unique(self.A[self.NEST.A==u])  for u in self.NEST.u]
		self.n          = [u.size for u in self.u]

	def _01_check_unbalanced(self):
		pass
		# nn  = [(self.A==uu).sum()   for uu in self.u]
		# self.balanced = np.all( nn==nn[0] )

	def get_Q(self):
		Q = []
		for u in self.u:
			for uu in u:
				q = np.matrix(np.diag(self.A==uu), dtype=float)
				Q.append(q)
		return Q
	
	
	def get_design_main(self):
		A,B   = self.NEST.A, self.A
		X     = []
		for uA,UB in zip(self.NEST.u, self.u):
			for uB in UB[1:]:
				x        = np.zeros(self.J)
				x[(A==uA) & (B==uB)] = 1
				X.append(x)
		return np.matrix( X ).T
		

	def get_design_interaction(self, other):
		A,B,S  = self.NEST.A, other.A, self.A
		X      = []
		for uA,US in zip(self.NEST.u, self.u):
			for uB in other.u[1:]:
				for uS in US[1:]:
					x      = np.zeros(self.J)
					x[(A==uA)&(B==uB)&(S==uS)] =  1
					X.append(x)
		return np.matrix(X).T


	def get_design_interaction_3way(self, other, another):
		A,B,C,S  = self.NEST.A, other.A, another.A, self.A
		X        = []
		for uA,US in zip(self.NEST.u, self.u):
			for uB in other.u[1:]:
				for uC in another.u[1:]:
					for uS in US[1:]:
						x      = np.zeros(self.J)
						x[(A==uA)&(B==uB)&(C==uC)&(S==uS)] =  1
						X.append(x)
		return np.matrix(X).T




class FactorNested2(Factor):
	def __init__(self, A, nestfactor):
		pass
		self.NEST0      = nestfactor.NEST
		self.NEST1      = nestfactor
		super(FactorNested2, self).__init__(A)


	def _00_parse(self):
		A,B,C           = self.NEST0.A, self.NEST1.A, self.A
		uA,UB           = self.NEST0.u, self.NEST1.u
		self.J          = self.A.size
		self.u          = [[np.unique(C[(A==uuA)&(B==uuB)]) for uuB in uB]  for uuA,uB in zip(uA, UB)]
		self.n          = [[uu.size for uu in u] for u in self.u]

	def _01_check_unbalanced(self):
		pass

	def get_Q(self):
		Q = []
		for u in self.u:
			for uu in u:
				for uuu in uu:
					q = np.matrix(np.diag(self.A==uuu), dtype=float)
					Q.append(q)
		return Q

	def get_design_main(self):
		A,B,C = self.NEST0.A, self.NEST1.A, self.A
		X     = []
		for uA,UB,UUC in zip(self.NEST0.u, self.NEST1.u, self.u):
			for uB,UC in zip(UB, UUC):
				for uC in UC[1:]:
					x        = np.zeros(self.J)
					x[(A==uA) & (B==uB) & (C==uC)] = 1
					X.append(x)
		return np.matrix( X ).T




class FactorNestedTwoWay(Factor):
	def __init__(self, SUBJ, A, B):
		self.NEST0      = A
		self.NEST1      = B
		super(FactorNestedTwoWay, self).__init__(SUBJ)


	def _00_parse(self):
		A,B,S           = self.NEST0.A, self.NEST1.A, self.A
		uA,uB           = self.NEST0.u, self.NEST1.u
		self.J          = self.A.size
		self.u          = [[np.unique( S[(A==uuA)&(B==uuB)] )  for uuB in uB] for uuA in uA]
		self.n          = [[uu.size for uu in u] for u in self.u]

	def _01_check_unbalanced(self):
		pass

	def get_Q(self):
		pass
		
	def get_design_main(self):
		A,B,S    = self.NEST0.A, self.NEST1.A, self.A
		uA,uB,uS = np.unique(A), np.unique(B), np.unique(S)
		X        = []
		for uuA in uA:
			for uuB in uB:
				uS  = np.unique(S[(A==uuA) & (B==uuB)])
				for uuS in uS[1:]:
					x        = np.zeros(self.J)
					x[(A==uuA) & (B==uuB) & (S==uuS)] = 1
					X.append(x)
		return np.matrix( X ).T


	def get_design_interaction(self, other):
		A,B,C,S  = self.NEST0.A, self.NEST1.A, other.A, self.A
		X        = []
		for uA in self.NEST0.u:
			for uB in self.NEST1.u[1:]:
				for uC in other.u:
					uS = np.unique( S[(A==uA)&(B==uB)&(C==uC)] )
					for uuS in uS[1:]:
						x      = np.zeros(self.J)
						x[(A==uA)&(B==uB)&(C==uC)&(S==uuS)] =  1
						X.append(x)
		return np.matrix(X).T




