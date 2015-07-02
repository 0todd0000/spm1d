

import numpy as np
from matplotlib import pyplot




class Factor(object):
	def __init__(self, A):
		self.A          = np.asarray(A, dtype=int)        #integer vector of factor levels
		self.J          = None     #number of observations
		self.u          = None     #unique levels
		self.n          = None     #number of levels
		self.pairs      = None     #pairs of factor levels
		self.nPairs     = None     #number of factor-level pairs
		self.isnested   = False    #nested flag
		self.isrm       = False    #repeated measures flag
		self.nested     = None
		self.balanced   = True
		self._00_parse()
		self._01_check_unbalanced()

	def _00_parse(self):
		self.J            = self.A.size
		self.u            = np.unique(self.A)
		self.n            = self.u.size
		self.pairs        = np.vstack([self.u[:-1], self.u[1:]]).T
		if self.n>4:  ### add a redundant term
			self.pairs    = np.vstack([self.pairs, self.u[[-1,0]] ])
		self.nPairs       = self.pairs.shape[0]
		
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
			UA  = np.unique(A[S==uS])
			for uA in UA:
				N.append( ((S==uS) & (A==uA)).sum()  )
		return np.all( N==N[0] )



	def get_Q(self):
		return [np.matrix(np.diag(self.A==u), dtype=float) for u in self.u]
	
	def get_design_interaction(self, other):
		XAB        = []
		A,B        = self.A, other.A
		for uA0,uA1 in self.pairs:
			for uB0,uB1 in other.pairs:
				x      = np.zeros(self.J)
				x[(A==uA0)&(B==uB0)] =  1
				x[(A==uA0)&(B==uB1)] = -1
				x[(A==uA1)&(B==uB0)] = -1
				x[(A==uA1)&(B==uB1)] =  1
				XAB.append(x)
		return np.matrix(XAB).T




	
	def get_design_interaction_3way(self, other, another):
		XABC       = []
		A,B,C      = self.A, other.A, another.A
		pA,pB,pC   = self.pairs, other.pairs, another.pairs
		for uA0,uA1 in pA:
			for uB0,uB1 in pB:
				for uC0,uC1 in pC:
					x      = np.zeros(self.J)
					### part one:
					x[(A==uA0)&(B==uB0)&(C==uC0)] =  1
					x[(A==uA0)&(B==uB0)&(C==uC1)] = -1
					x[(A==uA0)&(B==uB1)&(C==uC0)] = -1
					x[(A==uA0)&(B==uB1)&(C==uC1)] =  1
					### part two:
					x[(A==uA1)&(B==uB0)&(C==uC0)] = -1
					x[(A==uA1)&(B==uB0)&(C==uC1)] =  1
					x[(A==uA1)&(B==uB1)&(C==uC0)] =  1
					x[(A==uA1)&(B==uB1)&(C==uC1)] = -1
					XABC.append(x)
		return np.matrix(XABC).T

	def get_design_main(self, simplified=False):
		X = []
		if simplified:
			for u in self.u:
				x     = np.zeros(self.J)
				x[self.A==u] = 1
				X.append(x)
		else:
			for u0,u1 in self.pairs:
				x        = np.zeros(self.J)
				x[self.A==u0] =  1
				x[self.A==u1] = -1
				X.append(x)
		return np.matrix( X ).T




class FactorSubject(Factor):
	def __init__(self, S):
		super(FactorSubject, self).__init__(S)




class FactorRM(Factor):
	def __init__(self, A, S):
		super(FactorRM, self).__init__(A)
		self.S     = S
		self.isrm  = True

	def get_design_subject_pooled(self):
		return self.S.get_design_main(simplified=True)
		
	def get_design_subject_partitioned(self):
		XS        = []
		for u0,u1 in self.pairs:
			for u in self.S.u:
				x    = np.zeros(self.J)
				x[(self.A==u0) & (self.S.A==u)] = +1
				x[(self.A==u1) & (self.S.A==u)] = -1
				XS.append(x)
		return np.matrix(XS).T


	def get_design_subject_partitioned3(self, other):
		XS        = []
		B,C       = self.A, other.A
		for uB0,uB1 in self.pairs:
			for uC0,uC1 in other.pairs:
				for u in self.S.u:
					x    = np.zeros(self.J)
					x[(B==uB0) & (C==uC0) & (self.S.A==u)]  = +1
					x[(B==uB0) & (C==uC1) & (self.S.A==u)]  = -1
					x[(B==uB1) & (C==uC0) & (self.S.A==u)]  = -1
					x[(B==uB1) & (C==uC1) & (self.S.A==u)]  = +1
					XS.append(x)
		return np.matrix(XS).T
			
			
	def get_design_subject_interaction(self, other):
		XS        = []
		A,B,S     = self.A, other.A, self.S.A
		for uA0,uA1 in self.pairs:
			for uB0,uB1 in other.pairs:
				for u in self.S.u:
					x    = np.zeros(self.J)
					x[(A==uA0)&(B==uB0) & (S==u)] = +1
					x[(A==uA0)&(B==uB1) & (S==u)] = -1
					x[(A==uA1)&(B==uB0) & (S==u)] = -1
					x[(A==uA1)&(B==uB1) & (S==u)] = +1
					XS.append(x)
		return np.matrix(XS).T





class FactorNested(Factor):
	def __init__(self, A, nestfactor):
		self.NEST       = nestfactor
		super(FactorNested, self).__init__(A)


	def _00_parse(self):
		self.J          = self.A.size
		self.u          = [np.unique(self.A[self.NEST.A==u])  for u in self.NEST.u]
		self.n          = [u.size for u in self.u]
		self.pairs      = [np.vstack([u[:-1], u[1:]]).T   for u in self.u]
		self.nPairs     = [pair.shape[0]  for pair in self.pairs]

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
		for u,pairs in zip(self.NEST.u, self.pairs):
			for u0,u1 in pairs:
				x        = np.zeros(self.J)
				x[(A==u)&(B==u0)] =  1
				x[(A==u)&(B==u1)] = -1
				X.append(x)
		return np.matrix( X ).T



class FactorNested2(Factor):
	def __init__(self, A, nestfactor):
		self.NEST0      = nestfactor.NEST
		self.NEST1      = nestfactor
		super(FactorNested2, self).__init__(A)


	def _00_parse(self):
		A,B,C           = self.NEST0.A, self.NEST1.A, self.A
		uA,UB           = self.NEST0.u, self.NEST1.u
		self.J          = self.A.size
		self.u          = [[np.unique(C[(A==uuA)&(B==uuB)]) for uuB in uB]  for uuA,uB in zip(uA, UB)]
		self.n          = [[uu.size for uu in u] for u in self.u]
		self.pairs      = [[np.vstack([uu[:-1], uu[1:]]).T   for uu in u] for u in self.u]
		self.nPairs     = [[p.shape[0]  for p in pair] for pair in self.pairs]

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
		for uA,UB,PAIRSC in zip(self.NEST0.u, self.NEST1.u, self.pairs):
			for uB,pairsC in zip(UB,PAIRSC):
				for u0,u1 in pairsC:
					x        = np.zeros(self.J)
					x[(A==uA)&(B==uB)&(C==u0)] =  1
					x[(A==uA)&(B==uB)&(C==u1)] =  -1
					X.append(x)
		return np.matrix( X ).T


