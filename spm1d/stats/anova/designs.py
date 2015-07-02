

import numpy as np
from matplotlib import pyplot


from factors import Factor,FactorNested,FactorNested2,FactorRM,FactorSubject
from modelbuilder import ModelBuilder


class _Design(object):
	def _get_column_const(self):
		return np.matrix( np.ones(self.J) ).T


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
	def __init__(self, A):
		self.X          = None       #design matrix
		self.A          = Factor(A)  #factor levels
		self.J          = self.A.J   #number of observations
		self.contrasts  = None       #contrast matrices
		self._assemble()
		
	

	def _assemble(self):
		### assemble design matrix columns:
		XA             = self.A.get_design_main()
		XCONST         = self._get_column_const()
		### specify model and add design matrix columns:
		model          = ModelBuilder(labels=['A', 'CONST'])
		model.add_main_columns('A', XA)
		model.add_main_columns('CONST', XCONST)
		### assemble design matrix and contrasts:
		self.X         = model.get_design_matrix()
		self.contrasts = [model.get_contrast('A')]



	def set_simplified_design(self, with_const=True, difference_contrasts=True):
		# if self.unbalanced:
		# 	raise( ValueError('ANOVA error: unable to simplify unbalanced designs') )
		# self._set_simplified_design_matrix(with_const)
		# self._set_simplified_contrast()
		if with_const:
			XA             = self.A.get_design_main(simplified=True)
			XCONST         = self._get_column_const()
			model          = ModelBuilder(labels=['A', 'CONST'])
			model.add_main_columns('A', XA)
			model.add_main_columns('CONST', XCONST)
		else:
			XA             = self.A.get_design_main(simplified=True)
			model          = ModelBuilder(labels=['A'])
			model.add_main_columns('A', XA)
		### assemble design matrix and contrasts:
		self.X         = model.get_design_matrix()
		if difference_contrasts:
			self.contrasts = [model.get_contrast_difference('A')]
		else:
			self.contrasts = [model.get_contrast('A')]







class ANOVA1rm(_Design):
	def __init__(self, A, SUBJ):
		self.X          = None          #design matrix
		self.S          = FactorSubject(SUBJ)  #subjects
		self.A          = FactorRM(A, self.S)  #factor levels
		self.J          = self.A.J      #number of observations
		self.contrasts  = None          #contrast matrices
		self._check_balanced()
		self._assemble()


	def _assemble(self):
		### assemble design matrix columns:
		XA             = self.A.get_design_main()
		XCONST         = self._get_column_const()
		XSA            = self.A.get_design_subject_pooled()
		### specify model and add design matrix columns:
		model          = ModelBuilder(labels=['A', 'CONST'], labels_subj=['SA'])
		model.add_main_columns('A', XA)
		model.add_main_columns('CONST', XCONST)
		model.add_subj_columns('SA', XSA)
		### assemble design matrix and contrasts:
		self.X         = model.get_design_matrix()
		self.contrasts = [model.get_contrast('A')]

	def _check_balanced(self):
		if not (self.A.balanced and self.S.balanced):
			raise( ValueError('Design must be balanced.') )
		if not self.S.check_balanced(self.A):
			raise( ValueError('Design must be balanced.') )







class ANOVA2(_Design):
	def __init__(self, A, B):
		self.X          = None       #design matrix
		self.A          = Factor(A)  #factor level vector
		self.B          = Factor(B)  #factor level vector
		self.J          = self.A.J   #number of observations
		self.contrasts  = None
		self.balanced   = True
		self._check_balanced()
		self._assemble()

	def _assemble(self):
		### assemble design matrix columns:
		XA             = self.A.get_design_main()
		XB             = self.B.get_design_main()
		XAB            = self.A.get_design_interaction(self.B)
		XCONST         = self._get_column_const()
		### specify model and add design matrix columns:
		model          = ModelBuilder(labels=['A', 'B', 'AB', 'CONST'])
		model.add_main_columns('A',  XA)
		model.add_main_columns('B',  XB)
		model.add_main_columns('AB', XAB)
		model.add_main_columns('CONST', XCONST)
		### assemble design matrix and contrasts:
		self.X         = model.get_design_matrix()
		self.contrasts = [model.get_contrast(s)  for s in ['A','B','AB']]

	def _check_balanced(self):
		if not (self.A.balanced and self.B.balanced):
			self.balanced = False
			raise( ValueError('Design must be balanced.') )
		if not self.A.check_balanced(self.B):
			self.balanced = False
			raise( ValueError('Design must be balanced.') )





class ANOVA2nested(ANOVA2):
	def __init__(self, A, B):
		self.X          = None
		self.A          = Factor(A)
		self.B          = FactorNested(B, self.A)
		self.J          = self.A.J
		self.contrasts  = None
		self._check_balanced()
		self._assemble()

	def _assemble(self):
		### assemble design matrix columns:
		XA             = self.A.get_design_main()
		XB             = self.B.get_design_main()
		XCONST         = self._get_column_const()
		### specify model and add design matrix columns:
		model          = ModelBuilder(labels=['A', 'B', 'CONST'])
		model.add_main_columns('A',  XA)
		model.add_main_columns('B',  XB)
		model.add_main_columns('CONST', XCONST)
		### assemble design matrix and contrasts:
		self.X         = model.get_design_matrix()
		self.contrasts = [model.get_contrast(s)  for s in ['A','B']]

	def _check_balanced(self):
		if not (self.A.balanced and self.B.balanced):
			raise( ValueError('Design must be balanced.') )
		if not self.A.check_balanced_nested(self.B):
			raise( ValueError('Design must be balanced.') )



class ANOVA2rm(ANOVA2):
	'''Both A and B are RM factors.'''
	def __init__(self, A, B, SUBJ):
		self.X          = None
		self.S          = FactorSubject(SUBJ)
		self.A          = FactorRM(A, self.S)
		self.B          = FactorRM(B, self.S)
		self.J          = self.A.J
		self.contrasts  = None
		self._check_balanced()
		self._assemble()

	def _assemble(self):
		### assemble design matrix columns:
		XA              = self.A.get_design_main()
		XB              = self.B.get_design_main()
		XAB             = self.A.get_design_interaction(self.B)
		XCONST          = self._get_column_const()
		XSA             = self.A.get_design_subject_partitioned()
		XSB             = self.B.get_design_subject_partitioned()
		XSAB            = self.A.get_design_subject_interaction(self.B)
		XSpooled        = self.A.get_design_subject_pooled()
		### specify model and add design matrix columns:
		model           = ModelBuilder(labels=['A', 'B', 'AB', 'CONST'], labels_subj=['SA', 'SB', 'SAB', 'SPOOLED'])
		model.add_main_columns('A', XA)
		model.add_main_columns('B', XB)
		model.add_main_columns('AB', XAB)
		model.add_main_columns('CONST', XCONST)
		model.add_subj_columns('SA', XSA)
		model.add_subj_columns('SB', XSB)
		model.add_subj_columns('SAB', XSAB)
		model.add_subj_columns('SPOOLED', XSpooled)
		### assemble design matrix and contrasts:
		self.X         = model.get_design_matrix()
		self.contrasts = [model.get_contrast_compound(s, ss)  for s,ss in [('A','SA'),('B','SB'),('AB','SAB')]]
		
	def _check_balanced(self):
		if not (self.A.balanced and self.B.balanced and self.S.balanced):
			raise( ValueError('Design must be balanced.') )
		if not self.A.check_balanced(self.B):
			raise( ValueError('Design must be balanced.') )
		if not self.S.check_balanced(self.A):
			raise( ValueError('Design must be balanced.') )
		if not self.S.check_balanced(self.B):
			raise( ValueError('Design must be balanced.') )

class ANOVA2onerm(ANOVA2rm):
	'''Only B is an RM factor.'''
	def _assemble(self):
		### assemble design matrix columns:
		XA              = self.A.get_design_main()
		XB              = self.B.get_design_main()
		XAB             = self.A.get_design_interaction(self.B)
		XCONST          = self._get_column_const()
		XSApooled       = self.A.get_design_subject_pooled()
		XSB             = self.B.get_design_subject_partitioned()
		### specify model and add design matrix columns:
		model           = ModelBuilder(labels=['A', 'B', 'AB', 'CONST'], labels_subj=['SApooled', 'SB'])
		model.add_main_columns('A', XA)
		model.add_main_columns('B', XB)
		model.add_main_columns('AB', XAB)
		model.add_main_columns('CONST', XCONST)
		model.add_subj_columns('SApooled', XSApooled)
		model.add_subj_columns('SB', XSB)
		### assemble design matrix and contrasts:
		self.X         = model.get_design_matrix()
		self.contrasts = [model.get_contrast_compound(s, ss)  for s,ss in [('A','SApooled'),('B','SB'),('AB','SB')]]


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
	def __init__(self, A, B, C):
		self.X          = None       #design matrix
		self.A          = Factor(A)  #factor level vector
		self.B          = Factor(B)  #factor level vector
		self.C          = Factor(C)  #factor level vector
		self.J          = self.A.J   #number of observations
		self.contrasts  = None
		self._check_balanced()
		self._assemble()

	def _assemble(self):
		### assemble design matrix columns:
		XA             = self.A.get_design_main()
		XB             = self.B.get_design_main()
		XC             = self.C.get_design_main()
		XAB            = self.A.get_design_interaction(self.B)
		XAC            = self.A.get_design_interaction(self.C)
		XBC            = self.B.get_design_interaction(self.C)
		XABC           = self.A.get_design_interaction_3way(self.B, self.C)
		XCONST         = self._get_column_const()
		### specify model and add design matrix columns:
		model          = ModelBuilder(labels=['A', 'B', 'C', 'AB', 'AC', 'BC', 'ABC', 'CONST'])
		model.add_main_columns('A',  XA)
		model.add_main_columns('B',  XB)
		model.add_main_columns('C',  XC)
		model.add_main_columns('AB', XAB)
		model.add_main_columns('AC', XAC)
		model.add_main_columns('BC', XBC)
		model.add_main_columns('ABC', XABC)
		model.add_main_columns('CONST', XCONST)
		### assemble design matrix and contrasts:
		self.X         = model.get_design_matrix()
		self.contrasts = [model.get_contrast(s)  for s in ['A', 'B', 'C', 'AB', 'AC', 'BC', 'ABC']]

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
	def __init__(self, A, B, C):
		self.X          = None
		self.A          = Factor(A)
		self.B          = FactorNested(B, self.A)
		self.C          = FactorNested2(C, self.B)
		self.J          = self.A.J
		self.contrasts  = None
		self._check_balanced()
		self._assemble()

	def _assemble(self):
		### assemble design matrix columns:
		XA             = self.A.get_design_main()
		XB             = self.B.get_design_main()
		XC             = self.C.get_design_main()
		XCONST         = self._get_column_const()
		### specify model and add design matrix columns:
		model          = ModelBuilder(labels=['A', 'B', 'C', 'CONST'])
		model.add_main_columns('A',  XA)
		model.add_main_columns('B',  XB)
		model.add_main_columns('C',  XC)
		model.add_main_columns('CONST', XCONST)
		### assemble design matrix and contrasts:
		self.X         = model.get_design_matrix()
		self.contrasts = [model.get_contrast(s)  for s in ['A','B', 'C']]

	def _check_balanced(self):
		if not (self.A.balanced and self.B.balanced and self.C.balanced):
			raise( ValueError('Design must be balanced.') )
		if not self.A.check_balanced_nested3(self.B, self.C):
			raise( ValueError('Design must be balanced.') )



class ANOVA3rm(ANOVA3):
	'''A, B and C are all RM factors (not yet implemented).'''
	pass



class ANOVA3onerm(ANOVA3rm):
	'''Only C is an RM factor.'''
	def __init__(self, A, B, C, SUBJ):
		self.X          = None
		self.S          = FactorSubject(SUBJ)
		self.A          = FactorRM(A, self.S)
		self.B          = FactorRM(B, self.S)
		self.C          = FactorRM(C, self.S)
		self.J          = self.A.J
		self.contrasts  = None
		self._swap      = self.A.n > self.B.n   ### swap A and B factors if needed
		self._check_balanced()
		self._swapAB()
		self._assemble()
		self._swapAB()
			

	def _assemble(self):
		### assemble design matrix columns:
		XA              = self.A.get_design_main()
		XB              = self.B.get_design_main()
		XC              = self.C.get_design_main()
		XAB             = self.A.get_design_interaction(self.B)
		XAC             = self.A.get_design_interaction(self.C)
		XBC             = self.B.get_design_interaction(self.C)
		XABC            = self.A.get_design_interaction_3way(self.B, self.C)
		XCONST          = self._get_column_const()
		XSpooled        = self.A.get_design_subject_pooled()
		XSC             = self.C.get_design_subject_partitioned()
		### specify model and add design matrix columns:
		model           = ModelBuilder(labels=['A','B','C', 'AB','AC','BC', 'ABC', 'CONST'], labels_subj=['Spooled', 'SC'])
		model.add_main_columns('A', XA)
		model.add_main_columns('B', XB)
		model.add_main_columns('C', XC)
		model.add_main_columns('AB', XAB)
		model.add_main_columns('AC', XAC)
		model.add_main_columns('BC', XBC)
		model.add_main_columns('ABC', XABC)
		model.add_main_columns('CONST', XCONST)
		model.add_subj_columns('Spooled', XSpooled)
		model.add_subj_columns('SC', XSC)
		### assemble design matrix and contrasts:
		self.X         = model.get_design_matrix()
		if self._swap:
			sspairs        = [('B','Spooled'), ('A','Spooled'), ('C','SC')]
			sspairs       += [('AB','Spooled'), ('BC','SC'), ('AC','SC')]
			sspairs       += [('ABC','SC')]
		else:
			sspairs        = [('A','Spooled'), ('B','Spooled'), ('C','SC')]
			sspairs       += [('AB','Spooled'), ('AC','SC'), ('BC','SC')]
			sspairs       += [('ABC','SC')]
		self.contrasts = [model.get_contrast_compound(s, ss)  for s,ss in sspairs]

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




class ANOVA3tworm(ANOVA3rm):
	'''Both B and C are RM factors.'''
	def __init__(self, A, B, C, SUBJ):
		self.X          = None
		self.S          = FactorSubject(SUBJ)
		self.A          = FactorRM(A, self.S)
		self.B          = FactorRM(B, self.S)
		self.C          = FactorRM(C, self.S)
		self.J          = self.A.J
		self.contrasts  = None
		self._swap      = self.B.n > self.C.n   ### swap B and C factors if needed
		self._check_balanced()
		self._swapBC()
		self._assemble()
		self._swapBC()
		
		
	def _assemble(self):
		### assemble design matrix columns:
		XA              = self.A.get_design_main()
		XB              = self.B.get_design_main()
		XC              = self.C.get_design_main()
		XAB             = self.A.get_design_interaction(self.B)
		XAC             = self.A.get_design_interaction(self.C)
		XBC             = self.B.get_design_interaction(self.C)
		XABC            = self.A.get_design_interaction_3way(self.B, self.C)
		XCONST          = self._get_column_const()
		XSpooled        = self.A.get_design_subject_pooled()
		XSB             = self.B.get_design_subject_partitioned()
		XSC             = self.C.get_design_subject_partitioned()
		XSBC            = self.B.get_design_subject_partitioned3(self.C)
		### specify model and add design matrix columns:
		model           = ModelBuilder(labels=['A','B','C', 'AB','AC','BC', 'ABC', 'CONST'], labels_subj=['Spooled', 'SB', 'SC', 'SBC'])
		model.add_main_columns('A', XA)
		model.add_main_columns('B', XB)
		model.add_main_columns('C', XC)
		model.add_main_columns('AB', XAB)
		model.add_main_columns('AC', XAC)
		model.add_main_columns('BC', XBC)
		model.add_main_columns('ABC', XABC)
		model.add_main_columns('CONST', XCONST)
		model.add_subj_columns('Spooled', XSpooled)
		model.add_subj_columns('SB', XSB)
		model.add_subj_columns('SC', XSC)
		model.add_subj_columns('SBC', XSBC)
		### assemble design matrix and contrasts:
		self.X         = model.get_design_matrix()
		if self._swap:
			sspairs    = [('A','Spooled'), ('C','SC'), ('B','SB')]
			sspairs   += [('AC','SC'), ('AB','SB'), ('BC','SBC')]
			sspairs   += [('ABC', 'SBC')]
		else:
			sspairs    = [('A','Spooled'), ('B','SB'), ('C','SC')]
			sspairs   += [('AB','SB'), ('AC','SC'), ('BC','SBC')]
			sspairs   += [('ABC', 'SBC')]

		self.contrasts = [model.get_contrast_compound(s, ss)  for s,ss in sspairs]


	def _swapBC(self):
		if self._swap:
			B,C         = self.C, self.B
			self.B      = B
			self.C      = C

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



