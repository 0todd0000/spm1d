
import numpy as np
from .. import _base


def _here_stack(Y):
	m,n  = Y.shape
	y    = np.hstack( Y.T )
	A    = np.hstack(  [ [i]*m for i in range(n) ]  )
	SUBJ = np.hstack(  list(range(m)) * n  )
	return y, A, SUBJ






class Abdi2010(_base.DatasetANOVA1rm):
	def _set_values(self):
		self.cite    = 'Abdi H (2010). The Greenhouse-Geisser correction. In Neil Salkind (Ed.), Encyclopedia of Research Design. Thousand Oaks, CA: Sage. 2010'
		self.www     = 'https://www.utdallas.edu/~herve/abdi-GreenhouseGeisser2010-pretty.pdf'
		
		Y  = np.array([
			[76, 64, 34, 26],
			[60, 48, 46, 30],
			[58, 34, 32, 28],
			[46, 46, 32, 28],
			[30, 18, 36, 28],
		])
		Y, A, SUBJ = _here_stack(Y)
		self.Y     = Y
		self.A     = A
		self.SUBJ  = SUBJ
		self.z     = 5.36
		self.df    = (3, 12)
		self.dfGG  = 1.34, 5.35
		self.dfGGX = 1, 4
		self.dfHF  = 1.76, 7.04
		self.p     = 0.018
		self.pGG   = 0.059
		self.pGGX  = 0.081
		self.pHF   = 0.041



class Groceries(_base.DatasetANOVA1rm):
	def _set_values(self):
		self.datafile = 'http://ww2.coastal.edu/kingw/statistics/R-tutorials/text/groceries.txt'
		self.www      = 'http://ww2.coastal.edu/kingw/statistics/R-tutorials/repeated.html'
		Y  = np.array([
			[1.17, 1.78, 1.29, 1.29],
			[1.77, 1.98, 1.99, 1.99],
			[1.49, 1.69, 1.79, 1.59],
			[0.65, 0.99, 0.69, 1.09],
			[1.58, 1.70, 1.89, 1.89],
			[3.13, 3.15, 2.99, 3.09],
			[2.09, 1.88, 2.09, 2.49],
			[0.62, 0.65, 0.65, 0.69],
			[5.89, 5.99, 5.99, 6.99],
			[4.46, 4.84, 4.99, 5.15],
		])
		Y, A, SUBJ = _here_stack(Y)
		self.Y     = Y
		self.A     = A
		self.SUBJ  = SUBJ
		self.z     = 4.344
		self.df    = (3, 27)
		self.p     = 0.0127



class Imacelebrity(_base.DatasetANOVA1rm):
	def _set_values(self):
		self.www      = 'http://discoveringstatistics.com/docs/repeatedmeasures.pdf'
		Y  = np.array([
			[8, 7, 1, 6],
			[9, 5, 2, 5],
			[6, 2, 3, 8],
			[5, 3, 1, 9],
			[8, 4, 5, 8],
			[7, 5, 6, 7],
			[10, 2, 7, 2],
			[12, 6, 8, 1],
		])
		Y, A, SUBJ = _here_stack(Y)
		self.Y     = Y
		self.A     = A
		self.SUBJ  = SUBJ
		self.z     = 3.794
		self.df    = (3, 21)
		self.dfGG  = 1.599, 11.190
		self.dfGGX = 1, 7
		self.dfHF  = 1.997, 13.981
		self.p     = 0.026
		self.pGG   = 0.059
		self.pGGX  = 0.092
		self.pHF   = 0.048



class Southampton1rm(_base.DatasetANOVA1rm):
	def _set_values(self):
		self.www   = 'http://www.southampton.ac.uk/~cpd/anovas/datasets/Doncaster&Davey%20-%20Model%206_1%20One%20factor%20repeated%20measures.txt'
		self.Y     = np.array([-4.4297, 4.7513, 3.2971, -1.4606, 4.8458, 5.1163, 6.0739, -1.9225, 6.1542, 10.4794, 12.4438, 9.2150])
		self.A     = np.array([1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3])
		self.SUBJ  = np.array([1, 2, 3, 4, 1, 2, 3, 4, 1, 2, 3, 4])
		self.z     = 12.36
		self.df    = (2, 6)
		self.p     = 0.007







