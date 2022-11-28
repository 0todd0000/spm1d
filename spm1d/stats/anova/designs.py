
'''
High-level ANOVA designs.
'''

# Copyright (C) 2016  Todd Pataky



import warnings
import numpy as np
from matplotlib import pyplot
from . factors import Factor,FactorNested,FactorNested2,FactorNestedTwoWay #FactorRM,FactorSubject







class Contrasts(object):
	def __init__(self, C, term_labels):
		self.C           = np.asarray(C, dtype=float)     #contrast matrix
		self.term_labels = term_labels

	def plot(self, ax=None):
		ax  = pyplot.gca() if ax==None else ax
		ax.imshow(self.C, interpolation='nearest', cmap='gray', vmin=-1, vmax=1, aspect='auto')
		xskip   = self.C.shape[1] / 10 + 1
		yskip   = self.C.shape[0] / 10 + 1
		pyplot.setp(ax, xticks=range(0, self.C.shape[1], xskip), yticks=range(0, self.C.shape[0], yskip))




class DesignBuilder(object):
	
	nFactors         = 1
	
	def __init__(self, labels=[]):
		self.COLS    = []
		self.labels  = list(labels)
		self.n       = len(self.labels)   #number of main factors
		self.ncol    = 0  #number of main columns
		self.nTerms  = 0  #total number of model terms
		self.colD    = dict(zip(self.labels,  [None]*self.n))
		self.XD      = dict(zip(self.labels,  [None]*self.n))


	def add_main_columns(self, label, X):
		self.XD[label]   = X
		i0,n             = self.ncol, X.shape[1]
		self.colD[label] = np.arange(i0, i0+n)
		self.COLS.append( range(i0,i0+n) )
		self.ncol       += n
		self.nTerms     += 1

	def get_contrasts(self):
		C         = np.zeros( (self.nTerms, self.ncol) )
		for i,col in enumerate(self.COLS):
			C[i,col] = 1
		return Contrasts(C, self.labels)

	def get_design_matrix(self):
		X   = np.hstack([self.XD[label]  for label in self.labels])
		return X






class _Design(object):
	def _get_column_const(self):
		return np.matrix( np.ones(self.J) ).T

	def get_design_label(self):
		return self.__class__.__name__
	def get_effect_labels(self):
		return self.effect_labels
	
	
	def plot(self, ax=None, plot_contrasts=True, contrastnums=[0,1,2]):
		if plot_contrasts:
			ax0 = pyplot.axes([0.05,0.05,0.4,0.9])
		else:
			ax0 = pyplot.axes()
		# self.design.plot(ax=ax0)
		ax0.imshow(self.X, interpolation='nearest', cmap='gray', vmin=-1, vmax=1, aspect='auto')
		xskip   = self.X.shape[1] / 10 + 1
		yskip   = self.X.shape[0] / 10 + 1
		pyplot.setp(ax0, xticks=range(0, self.X.shape[1], xskip), yticks=range(0, self.J, yskip))
		### plot contrasts:
		if plot_contrasts and self.contrasts!=None:
			yy  = np.linspace(0.7, 0.05, 3)
			if len(self.contrasts) < 4:
				for i,contrast in enumerate(self.contrasts):
					ax  = pyplot.axes([0.53,yy[i],0.45,0.2])
					contrast.plot(ax=ax)
			else:
				for i,ci in enumerate(contrastnums):
					ax  = pyplot.axes([0.53,yy[i],0.45,0.2])
					self.contrasts[ci].plot(ax=ax)
		pyplot.show()





class ANOVA1(_Design):
	
	effect_labels        = ('Main A', )
	nFactors             = 1
	
	def __init__(self, A):
		self.X           = None       #design matrix
		self.A           = Factor(A)  #factor levels
		self.J           = self.A.J   #number of observations
		self.contrasts   = None       #contrast matrix
		self.term_labels = ['Intercept', 'A']
		self.f_terms     = [('A','Error')]
		self._assemble()
		
	

	def _assemble(self):
		### assemble design matrix columns:
		XCONST         = self._get_column_const()
		XA             = self.A.get_design_main()
		### specify builder and add design matrix columns:
		builder        = DesignBuilder(labels=self.term_labels)
		builder.add_main_columns('Intercept', XCONST)
		builder.add_main_columns('A', XA)
		### assemble design matrix and contrasts:
		self.X         = builder.get_design_matrix()
		self.contrasts = builder.get_contrasts()




class ANOVA1rm(_Design):
	
	effect_labels       = ('Main A', )
	nFactors            = 1
	
	def __init__(self, A, SUBJ):
		self.X          = None          #design matrix
		self.S          = Factor(SUBJ)  #subjects
		self.A          = Factor(A)     #factor levels
		self.J          = self.A.J      #number of observations
		self.contrasts  = None          #contrast matrix
		self.term_labels = ['Intercept', 'A', 'S', 'SA']
		self.f_terms     = [('A','SA')]
		self._check_balanced()
		self._assemble()


	def _assemble(self):
		### assemble design matrix columns:
		XCONST         = self._get_column_const()
		XA             = self.A.get_design_main()
		XS             = self.S.get_design_main()
		XSA            = self.A.get_design_interaction(self.S)
		### specify builder and add design matrix columns:
		builder        = DesignBuilder(labels=self.term_labels)
		builder.add_main_columns('Intercept', XCONST)
		builder.add_main_columns('A', XA)
		builder.add_main_columns('S', XS)
		builder.add_main_columns('SA', XSA)
		### assemble design matrix and contrasts:
		self.X         = builder.get_design_matrix()
		self.contrasts = builder.get_contrasts()

	def _check_balanced(self):
		if not (self.A.balanced and self.S.balanced):
			raise( ValueError('Design must be balanced.') )
		if not self.S.check_balanced(self.A):
			raise( ValueError('Design must be balanced.') )

	def check_for_single_responses(self, dim=1):
		A,S  = self.A.A, self.S.A
		only_single = False
		for a in self.A.u:
			s = S[(A==a)]
			if np.unique(s).size == s.size:
				only_single = True
				if dim==1:
					warnings.warn('\nWARNING:  Only one observation per subject found.  Residuals and inference will be approximate. To avoid approximate residuals: (a) Add multiple observations per subject and per condition, and (b) ensure that all subjects and conditions have the same number of observations.\n', UserWarning, stacklevel=2)
				continue
		return only_single





class ANOVA2(_Design):
	
	effect_labels        = ('Main A', 'Main B', 'Interaction AB')
	nFactors             = 2
	
	def __init__(self, A, B):
		self.X           = None       #design matrix
		self.A           = Factor(A)  #factor level vector
		self.B           = Factor(B)  #factor level vector
		self.J           = self.A.J   #number of observations
		self.contrasts   = None
		self.balanced    = True
		self.term_labels = ['Intercept', 'A', 'B', 'AB']
		self.f_terms     = [('A','Error'), ('B','Error'), ('AB','Error')]
		self._check_balanced()
		self._assemble()

	def _assemble(self):
		### assemble design matrix columns:
		XCONST         = self._get_column_const()
		XA             = self.A.get_design_main()
		XB             = self.B.get_design_main()
		XAB            = self.A.get_design_interaction(self.B)
		### specify builder and add design matrix columns:
		builder          = DesignBuilder(labels=self.term_labels)
		builder.add_main_columns('Intercept', XCONST)
		builder.add_main_columns('A',  XA)
		builder.add_main_columns('B',  XB)
		builder.add_main_columns('AB', XAB)
		### assemble design matrix and contrasts:
		self.X         = builder.get_design_matrix()
		self.contrasts = builder.get_contrasts()

	def _check_balanced(self):
		if not (self.A.balanced and self.B.balanced):
			self.balanced = False
			raise( ValueError('Design must be balanced.') )
		if not self.A.check_balanced(self.B):
			self.balanced = False
			raise( ValueError('Design must be balanced.') )





class ANOVA2nested(ANOVA2):
	
	effect_labels       = ('Main A', 'Main B')
	nFactors            = 2
	
	def __init__(self, A, B):
		self.X          = None
		self.A          = Factor(A)
		self.B          = FactorNested(B, self.A)
		self.J          = self.A.J
		self.contrasts  = None
		self.term_labels = ['Intercept', 'A', 'B']
		self.f_terms     = [('A','B'), ('B','Error')]
		self._check_balanced()
		self._assemble()

	def _assemble(self):
		### assemble design matrix columns:
		XCONST         = self._get_column_const()
		XA             = self.A.get_design_main()
		XB             = self.B.get_design_main()
		# XB             = self.B.get_design_main_nested(self.A)
		### specify builder and add design matrix columns:
		builder          = DesignBuilder(labels=['Intercept', 'A', 'B'])
		builder.add_main_columns('Intercept', XCONST)
		builder.add_main_columns('A',  XA)
		builder.add_main_columns('B',  XB)
		### assemble design matrix and contrasts:
		self.X         = builder.get_design_matrix()
		self.contrasts = builder.get_contrasts()

	def _check_balanced(self):
		if not (self.A.balanced and self.B.balanced):
			raise( ValueError('Design must be balanced.') )
		if not self.A.check_balanced_nested(self.B):
			raise( ValueError('Design must be balanced.') )



class ANOVA2rm(ANOVA2):
	'''Both A and B are RM factors.'''
	def __init__(self, A, B, SUBJ):
		self.X           = None
		self.S           = Factor(SUBJ)
		self.A           = Factor(A)
		self.B           = Factor(B)
		self.J           = self.A.J
		self.contrasts   = None
		self.term_labels = ['Intercept', 'A', 'B', 'S', 'AB', 'SA', 'SB', 'SAB']
		self.f_terms     = [('A','SA'), ('B','SB'), ('AB','SAB')]
		self._check_balanced()
		self._assemble()

	def _assemble(self):
		### assemble design matrix columns:
		XCONST          = self._get_column_const()
		XA              = self.A.get_design_main()
		XB              = self.B.get_design_main()
		XS              = self.S.get_design_main()
		XAB             = self.A.get_design_interaction(self.B)
		XSA             = self.A.get_design_interaction(self.S)
		XSB             = self.B.get_design_interaction(self.S)
		XSAB            = self.A.get_design_interaction_3way(self.B, self.S)
		### specify builder and add design matrix columns:
		builder           = DesignBuilder(labels=self.term_labels)
		builder.add_main_columns('Intercept', XCONST)
		builder.add_main_columns('A', XA)
		builder.add_main_columns('B', XB)
		builder.add_main_columns('S', XS)
		builder.add_main_columns('AB', XAB)
		builder.add_main_columns('SA', XSA)
		builder.add_main_columns('SB', XSB)
		builder.add_main_columns('SAB', XSAB)
		### assemble design matrix and contrasts:
		self.X         = builder.get_design_matrix()
		self.contrasts = builder.get_contrasts()


	def _check_balanced(self):
		if not (self.A.balanced and self.B.balanced and self.S.balanced):
			raise( ValueError('Design must be balanced.') )
		if not self.A.check_balanced(self.B):
			raise( ValueError('Design must be balanced.') )
		if not self.S.check_balanced(self.A):
			raise( ValueError('Design must be balanced.') )
		if not self.S.check_balanced(self.B):
			raise( ValueError('Design must be balanced.') )


	def check_for_single_responses(self, dim=1):
		A,B,S  = self.A.A, self.B.A, self.S.A
		only_single = False
		for a in self.A.u:
			for b in self.B.u:
				s = S[(A==a) & (B==b)]
				if np.unique(s).size == s.size:
					only_single = True
					if dim==1:
						warnings.warn('\nWARNING:  Only one observation per subject found.  Residuals and inference will be approximate. To avoid approximate residuals: (a) Add multiple observations per subject and per condition, and (b) ensure that all subjects and conditions have the same number of observations.\n', UserWarning, stacklevel=2)
					continue
		return only_single



class ANOVA2onerm(ANOVA2rm):
	'''Only B is an RM factor.'''
	def __init__(self, A, B, SUBJ):
		self.X           = None
		self.A           = Factor(A)
		self.B           = Factor(B)
		self.S           = FactorNested(SUBJ, self.A)
		self.J           = self.A.J
		self.contrasts   = None
		self.term_labels = ['Intercept', 'A', 'B', 'S', 'AB', 'SB']
		self.f_terms     = [('A','S'), ('B','SB'), ('AB','SB')]
		# self._check_balanced()
		self._assemble()

	def _assemble(self):
		### assemble design matrix columns:
		XCONST          = self._get_column_const()
		XA              = self.A.get_design_main()
		XB              = self.B.get_design_main()
		XS              = self.S.get_design_main()
		XAB             = self.A.get_design_interaction(self.B)
		XSB             = self.S.get_design_interaction(self.B)
		### specify builder and add design matrix columns:
		builder         = DesignBuilder(labels=self.term_labels)
		builder.add_main_columns('Intercept', XCONST)
		builder.add_main_columns('A', XA)
		builder.add_main_columns('B', XB)
		builder.add_main_columns('S', XS)
		builder.add_main_columns('AB', XAB)
		builder.add_main_columns('SB', XSB)
		### assemble design matrix and contrasts:
		self.X         = builder.get_design_matrix()
		self.contrasts = builder.get_contrasts()


	def _check_balanced(self):
		if not (self.A.balanced and self.B.balanced and self.S.balanced):
			raise( ValueError('Design must be balanced.') )
		if not self.A.check_balanced(self.B):
			raise( ValueError('Design must be balanced.') )
		if not self.S.check_balanced_rm(self.A):
			raise( ValueError('Design must be balanced.') )
		if not self.S.check_balanced_rm(self.B):
			raise( ValueError('Design must be balanced.') )










class ANOVA3(_Design):
	
	effect_labels       = ('Main A', 'Main B', 'Main C', 'Interaction AB', 'Interaction AC', 'Interaction BC','Interaction ABC')
	nFactors            = 3
	
	def __init__(self, A, B, C):
		self.X          = None       #design matrix
		self.A          = Factor(A)  #factor level vector
		self.B          = Factor(B)  #factor level vector
		self.C          = Factor(C)  #factor level vector
		self.J          = self.A.J   #number of observations
		self.term_labels = ['Intercept', 'A', 'B', 'C', 'AB', 'AC', 'BC', 'ABC']
		self.f_terms     = [('A','Error'), ('B','Error'), ('C','Error'), ('AB','Error'), ('AC','Error'), ('BC','Error'), ('ABC','Error')]
		self.contrasts  = None
		self._check_balanced()
		self._assemble()

	def _assemble(self):
		### assemble design matrix columns:
		XCONST         = self._get_column_const()
		XA             = self.A.get_design_main()
		XB             = self.B.get_design_main()
		XC             = self.C.get_design_main()
		XAB            = self.A.get_design_interaction(self.B)
		XAC            = self.A.get_design_interaction(self.C)
		XBC            = self.B.get_design_interaction(self.C)
		XABC           = self.A.get_design_interaction_3way(self.B, self.C)
		### specify builder and add design matrix columns:
		builder        = DesignBuilder(labels=['Intercept', 'A', 'B', 'C', 'AB', 'AC', 'BC', 'ABC'])
		builder.add_main_columns('Intercept', XCONST)
		builder.add_main_columns('A',  XA)
		builder.add_main_columns('B',  XB)
		builder.add_main_columns('C',  XC)
		builder.add_main_columns('AB', XAB)
		builder.add_main_columns('AC', XAC)
		builder.add_main_columns('BC', XBC)
		builder.add_main_columns('ABC', XABC)
		### assemble design matrix and contrasts:
		self.X         = builder.get_design_matrix()
		self.contrasts = builder.get_contrasts()


	def _check_balanced(self):
		if not (self.A.balanced and self.B.balanced and self.C.balanced):
			raise( ValueError('Design must be balanced.') )
		if not self.A.check_balanced(self.B):
			raise( ValueError('Design must be balanced.') )
		if not self.A.check_balanced(self.C):
			raise( ValueError('Design must be balanced.') )
		if not self.B.check_balanced(self.C):
			raise( ValueError('Design must be balanced.') )





class ANOVA3nested(ANOVA3):
	
	effect_labels       = ('Main A', 'Main B', 'Main C')
	
	def __init__(self, A, B, C):
		self.X          = None
		self.A          = Factor(A)
		self.B          = FactorNested(B, self.A)
		self.C          = FactorNested2(C, self.B)
		self.J          = self.A.J
		self.contrasts  = None
		self.term_labels = ['Intercept', 'A', 'B', 'C']
		self.f_terms     = [('A','B'), ('B','C'), ('C','Error')]
		self._check_balanced()
		self._assemble()

	def _assemble(self):
		### assemble design matrix columns:
		XCONST         = self._get_column_const()
		XA             = self.A.get_design_main()
		XB             = self.B.get_design_main()
		XC             = self.C.get_design_main()
		### specify builder and add design matrix columns:
		builder          = DesignBuilder(labels=['Intercept', 'A', 'B', 'C'])
		builder.add_main_columns('Intercept', XCONST)
		builder.add_main_columns('A',  XA)
		builder.add_main_columns('B',  XB)
		builder.add_main_columns('C',  XC)
		### assemble design matrix and contrasts:
		self.X         = builder.get_design_matrix()
		self.contrasts = builder.get_contrasts()

	def _check_balanced(self):
		if not (self.A.balanced and self.B.balanced and self.C.balanced):
			raise( ValueError('Design must be balanced.') )
		if not self.A.check_balanced_nested3(self.B, self.C):
			raise( ValueError('Design must be balanced.') )



class ANOVA3rm(ANOVA3):
	'''A, B and C are all RM factors.'''
	def __init__(self, A, B, C, SUBJ):
		self.X          = None
		self.A           = Factor(A)
		self.B           = Factor(B)
		self.C           = Factor(C)
		self.S           = Factor(SUBJ)
		self.J           = self.A.J
		self.contrasts   = None
		self.term_labels = ['Intercept',  'A','B','C','S',  'AB','AC','BC',   'SA','SB','SC',   'SAB','SAC','SBC',  'ABC', 'SABC']
		self.f_terms     = [('A','SA'), ('B','SB'), ('C','SC'),  ('AB','SAB'), ('AC','SAC'), ('BC','SBC'), ('ABC','SABC')]
		self._check_balanced()
		self._assemble()


	def _assemble(self):
		### assemble design matrix columns:
		XCONST          = self._get_column_const()
		XA              = self.A.get_design_main()
		XB              = self.B.get_design_main()
		XC              = self.C.get_design_main()
		XS              = self.S.get_design_main()
		XAB             = self.A.get_design_interaction(self.B)
		XAC             = self.A.get_design_interaction(self.C)
		XBC             = self.B.get_design_interaction(self.C)
		XSA             = self.S.get_design_interaction(self.A)
		XSB             = self.S.get_design_interaction(self.B)
		XSC             = self.S.get_design_interaction(self.C)
		XSAB            = self.S.get_design_interaction_3way(self.A, self.B)
		XSAC            = self.S.get_design_interaction_3way(self.A, self.C)
		XSBC            = self.S.get_design_interaction_3way(self.B, self.C)
		XABC            = self.A.get_design_interaction_3way(self.B, self.C)
		XSABC           = self.S.get_design_interaction_4way(self.A, self.B, self.C)
		### specify builder and add design matrix columns:
		builder           = DesignBuilder(labels=self.term_labels)
		builder.add_main_columns('Intercept', XCONST)
		builder.add_main_columns('A', XA)
		builder.add_main_columns('B', XB)
		builder.add_main_columns('C', XC)
		builder.add_main_columns('S', XS)
		builder.add_main_columns('AB', XAB)
		builder.add_main_columns('AC', XAC)
		builder.add_main_columns('BC', XBC)
		builder.add_main_columns('SA', XSA)
		builder.add_main_columns('SB', XSB)
		builder.add_main_columns('SC', XSC)
		builder.add_main_columns('SAB', XSAB)
		builder.add_main_columns('SAC', XSAC)
		builder.add_main_columns('SBC', XSBC)
		builder.add_main_columns('ABC', XABC)
		builder.add_main_columns('SABC', XSABC)
		### assemble design matrix and contrasts:
		self.X         = builder.get_design_matrix()
		self.contrasts = builder.get_contrasts()

	def _swapAB(self):
		if self._swap:
			A,B         = self.B, self.A
			self.A      = A
			self.B      = B

	def _check_balanced(self):
		if not (self.A.balanced and self.B.balanced and self.C.balanced and self.S.balanced):
			raise( ValueError('Design must be balanced.') )
		if not self.A.check_balanced(self.B):
			raise( ValueError('Design must be balanced.') )
		if not self.A.check_balanced(self.C):
			raise( ValueError('Design must be balanced.') )
		if not self.B.check_balanced(self.C):
			raise( ValueError('Design must be balanced.') )
		if not self.S.check_balanced_rm(self.C):
			raise( ValueError('Design must be balanced.') )


	def check_for_single_responses(self, dim=1):
		A,B,C,S  = self.A.A, self.B.A, self.C.A, self.S.A
		only_single = False
		for a in self.A.u:
			for b in self.B.u:
				for c in self.C.u:
					s = S[(A==a) & (B==b) & (C==c)]
					if np.unique(s).size == s.size:
						only_single = True
						if dim==1:
							warnings.warn('\nWARNING:  Only one observation per subject found.  Residuals and inference will be approximate. To avoid approximate residuals: (a) Add multiple observations per subject and per condition, and (b) ensure that all subjects and conditions have the same number of observations.\n', UserWarning, stacklevel=2)
						continue
		return only_single





class ANOVA3onerm(ANOVA3rm):
	'''Only C is an RM factor.'''
	def __init__(self, A, B, C, SUBJ):
		self.X           = None
		self.A           = Factor(A)
		self.B           = Factor(B)
		self.C           = Factor(C)
		self.S           = FactorNestedTwoWay(SUBJ, self.A, self.B)
		# self.S           = FactorNestedTwoWay(SUBJ, self.B, self.C)
		self.J           = self.A.J
		self.contrasts   = None
		self.term_labels = ['Intercept',  'A','B','C', 'AB','AC','BC',    'ABC', 'S', 'SC']
		self.f_terms     = [('A','S'), ('B','S'), ('C','SC'),  ('AB','S'), ('AC','SC'), ('BC','SC'), ('ABC','SC')]
		self._check_balanced()
		self._assemble()


	def _assemble(self):
		### assemble design matrix columns:
		XCONST          = self._get_column_const()
		XA              = self.A.get_design_main()
		XB              = self.B.get_design_main()
		XC              = self.C.get_design_main()
		XS              = self.S.get_design_main()
		XAB             = self.A.get_design_interaction(self.B)
		XAC             = self.A.get_design_interaction(self.C)
		XBC             = self.B.get_design_interaction(self.C)
		XABC            = self.C.get_design_interaction_3way(self.A, self.B)
		XSC             = self.S.get_design_interaction(self.C)
		### specify builder and add design matrix columns:
		builder           = DesignBuilder(labels=self.term_labels)
		builder.add_main_columns('Intercept', XCONST)
		builder.add_main_columns('A', XA)
		builder.add_main_columns('B', XB)
		builder.add_main_columns('C', XC)
		builder.add_main_columns('AB', XAB)
		builder.add_main_columns('AC', XAC)
		builder.add_main_columns('BC', XBC)
		builder.add_main_columns('ABC', XABC)
		builder.add_main_columns('S', XS)
		builder.add_main_columns('SC', XSC)
		### assemble design matrix and contrasts:
		self.X         = builder.get_design_matrix()
		self.contrasts = builder.get_contrasts()

	def _check_balanced(self):
		if not (self.A.balanced and self.B.balanced and self.C.balanced and self.S.balanced):
			raise( ValueError('Design must be balanced.') )
		if not self.A.check_balanced(self.B):
			raise( ValueError('Design must be balanced.') )
		if not self.A.check_balanced(self.C):
			raise( ValueError('Design must be balanced.') )
		if not self.B.check_balanced(self.C):
			raise( ValueError('Design must be balanced.') )
		if not self.S.check_balanced_rm(self.C):
			raise( ValueError('Design must be balanced.') )




class ANOVA3tworm(ANOVA3rm):
	'''Both B and C are RM factors.'''
	def __init__(self, A, B, C, SUBJ):
		self.X          = None
		self.A           = Factor(A)
		self.B           = Factor(B)
		self.C           = Factor(C)
		self.S           = FactorNested(SUBJ, self.A)
		# self.S           = FactorNestedTwoWay(SUBJ, self.B, self.C)
		self.J           = self.A.J
		self.contrasts   = None
		self.term_labels = ['Intercept',  'A','B','C','S',  'AB','AC','BC',  'SB','SC',   'ABC', 'SBC']
		self.f_terms     = [('A','S'), ('B','SB'), ('C','SC'),  ('AB','SB'), ('AC','SC'), ('BC','SBC'), ('ABC','SBC')]
		self._check_balanced()
		self._assemble()


	def _assemble(self):
		### assemble design matrix columns:
		XCONST          = self._get_column_const()
		XA              = self.A.get_design_main()
		XB              = self.B.get_design_main()
		XC              = self.C.get_design_main()
		XS              = self.S.get_design_main()
		XAB             = self.A.get_design_interaction(self.B)
		XAC             = self.A.get_design_interaction(self.C)
		XBC             = self.B.get_design_interaction(self.C)
		XSB             = self.S.get_design_interaction(self.B)
		XSC             = self.S.get_design_interaction(self.C)
		XABC            = self.A.get_design_interaction_3way(self.B, self.C)
		XSBC            = self.S.get_design_interaction_3way(self.B, self.C)
		### specify builder and add design matrix columns:
		builder           = DesignBuilder(labels=self.term_labels)
		builder.add_main_columns('Intercept', XCONST)
		builder.add_main_columns('A', XA)
		builder.add_main_columns('B', XB)
		builder.add_main_columns('C', XC)
		builder.add_main_columns('S', XS)
		builder.add_main_columns('AB', XAB)
		builder.add_main_columns('AC', XAC)
		builder.add_main_columns('BC', XBC)
		builder.add_main_columns('SB', XSB)
		builder.add_main_columns('SC', XSC)
		builder.add_main_columns('ABC', XABC)
		builder.add_main_columns('SBC', XSBC)
		### assemble design matrix and contrasts:
		self.X         = builder.get_design_matrix()
		self.contrasts = builder.get_contrasts()



	def _check_balanced(self):
		if not (self.A.balanced and self.B.balanced and self.C.balanced and self.S.balanced):
			raise( ValueError('Design must be balanced.') )
		if not self.A.check_balanced(self.B):
			raise( ValueError('Design must be balanced.') )
		if not self.A.check_balanced(self.C):
			raise( ValueError('Design must be balanced.') )
		if not self.B.check_balanced(self.C):
			raise( ValueError('Design must be balanced.') )
		if not self.S.check_balanced_rm(self.B):
			raise( ValueError('Design must be balanced.') )
		if not self.S.check_balanced_rm(self.C):
			raise( ValueError('Design must be balanced.') )





