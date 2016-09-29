
import numpy as np
from .. import _base





class Detergent(_base.DatasetANOVA2):
	def _set_values(self):
		self.www   = 'http://statweb.stanford.edu/~susan/courses/s141/exanova.pdf'
		self.Y     = np.array([4,5,6,5,   7,9,8,12,   10,12,11,9,    6,6,4,4,  13,15,12,12,   12,13,10,13])
		self.A     = np.array([0,0,0,0,   0,0,0,0,    0,0,0,0,       1,1,1,1,   1,1,1,1,      1,1,1,1,])
		self.B     = np.array([0,0,0,0,   1,1,1,1,    2,2,2,2,       0,0,0,0,   1,1,1,1,    2,2,2,2])
		self.z     = 9.81008, 48.7297, 3.9730
		self.df    = (1, 18), (2, 18), (2, 18)
		self.p     = 0.005758, 0.000, 0.037224

class Mouse(_base.DatasetANOVA2):
	def _set_values(self):
		self.www   = 'http://www4.uwsp.edu/psych/stat/13/anova-2w.htm'
		self.Y     = np.array([5,4,3,4,2,   6,7,5,8,4,    18,19,14,12,15,   6,9,5,9,3])
		self.A     = np.array([0,0,0,0,0,   0,0,0,0,0,    1,1,1,1,1,        1,1,1,1,1])
		self.B     = np.array([0,0,0,0,0,   1,1,1,1,1,    0,0,0,0,0,        1,1,1,1,1])
		self.z     = 40.68, 12.23, 35.60
		self.df    = (1, 16), (1, 16), (1, 16)
		self.p     = ('<0.05', '<0.05', '<0.05')


class Satisfaction(_base.DatasetANOVA2):
	def _set_values(self):
		self.www   = 'http://www2.webster.edu/~woolflm/8canswer.html'
		self.Y     = np.array([4,2,3,4,2,   7,5,7,5,6,    10,7,9,8,11,   7,4,3,6,5,  8,10,7,7,8,  10,9,12,11,13])
		self.A     = np.array([0,0,0,0,0,   0,0,0,0,0,    0,0,0,0,0,     1,1,1,1,1,  1,1,1,1,1,    1,1,1,1,1])
		self.B     = np.array([0,0,0,0,0,   1,1,1,1,1,    2,2,2,2,2,     0,0,0,0,0,  1,1,1,1,1,    2,2,2,2,2])
		self.z     = 16.36, 49.09, 0.00
		self.df    = (1, 24), (2, 24), (2, 24)
		self.p     = ('<0.01', '<0.01', '>0.05')

class SouthamptonCrossed1(_base.DatasetANOVA2):
	def _set_values(self):
		self.www     = 'http://www.southampton.ac.uk/~cpd/anovas/datasets/Doncaster&Davey%20-%20Model%203_1%20Two%20factor%20fully%20cross%20factored.txt'
		self.A       = np.array([1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3])
		self.B       = np.array([1, 1, 1, 1, 2, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2])
		self.Y       = np.array([4.5924, -0.5488, 6.1605, 2.3374, 5.1873, 3.3579, 6.3092, 3.2831, 7.3809, 9.2085, 13.1147, 15.2654, 12.4188, 14.3951, 8.5986, 3.4945, 21.3220, 25.0426, 22.6600, 24.1283, 16.5927, 10.2129, 9.8934, 10.0203])
		self.z       = 37.23, 9.16, 9.31
		self.df      = (2, 18), (1, 18), (2, 18)
		self.p       = '<0.001', 0.007, 0.002



class SPM1D3x3(_base.DatasetANOVA2):
	def _set_values(self):
		nSubj        = 5
		self.A       = np.array([0]*nSubj*3 + [1]*nSubj*3 + [2]*nSubj*3)
		self.B       = np.array([0,1,2]*nSubj*3)
		self.Y       = np.array([6, 2, 7, 1, 3, 5, 3, 4, 7, 7, 3, 5, 7, 9, 9, 0, 3, 1, 1, 9, 4, 7, 5, 0, 9, 4, 1, 8, 9, 6, 4, 5, 9, 8, 5, 3, 7, 3, 9, 1, 4, 5, 6, 4, 0])
		#results computed using R (r-project.org):  aov(Y ~ A + B + A*B)
		self.z       = 0.249, 0.036, 1.628
		self.df      = (2,36), (2,36), (4,36)
		self.p       = 0.781, 0.965, 0.188
		self._rtol   = 0.1

class SPM1D3x4(_base.DatasetANOVA2):
	def _set_values(self):
		nA,nB,nSubj  = 3,4,10
		self.A       = np.array([0]*nSubj*nB + [1]*nSubj*nB + [2]*nSubj*nB)
		self.B       = np.array( list(range(nB)) *nSubj*nA)
		self.Y       = np.array([2, 2, 5, 5, 4, 8, 6, 5, 5, 5, 0, 0, 6, 1, 0, 3, 6, 5, 7, 9, 4, 6, 7, 5, 1, 7, 4, 3, 4, 8, 6, 7, 8, 2, 0, 2, 9, 5, 1, 3, 9, 2, 7, 8, 9, 7, 4, 2, 3, 0, 1, 5, 0, 0, 6, 3, 7, 5, 3, 0, 8, 3, 4, 6, 9, 6, 0, 5, 9, 8, 5, 1, 7, 2, 4, 7, 0, 7, 5, 1, 1, 1, 0, 4, 3, 7, 4, 6, 7, 5, 9, 2, 0, 2, 3, 9, 1, 4, 6, 5, 8, 7, 4, 1, 3, 1, 7, 0, 0, 7, 0, 6, 2, 4, 0, 0, 6, 1, 3, 5])
		#results computed using R (r-project.org):  aov(Y ~ A + B + A*B)
		self.z       = 1.131, 0.703, 0.728
		self.df      = (2,108), (3,108), (6,108)
		self.p       = 0.327, 0.552, 0.628

class SPM1D3x5(_base.DatasetANOVA2):
	def _set_values(self):
		nA,nB,nSubj  = 3,5,7
		self.A       = np.array([0]*nSubj*nB + [1]*nSubj*nB + [2]*nSubj*nB)
		self.B       = np.array( list(range(nB)) *nSubj*nA)
		self.Y       = np.array([2, 6, 5, 0, 5, 1, 1, 5, 4, 0, 8, 8, 4, 7, 3, 0, 4, 7, 5, 7, 1, 3, 2, 3, 7, 3, 3, 0, 8, 6, 9, 3, 0, 7, 6, 5, 8, 8, 3, 5, 2, 2, 2, 6, 8, 7, 9, 8, 4, 8, 2, 4, 3, 8, 7, 2, 0, 8, 9, 5, 9, 4, 8, 0, 0, 6, 6, 8, 6, 7, 1, 8, 4, 4, 7, 7, 2, 6, 9, 6, 1, 8, 2, 5, 0, 9, 8, 7, 9, 4, 7, 9, 6, 9, 4, 6, 4, 2, 1, 4, 0, 8, 1, 8, 8])
		#results computed using R (r-project.org):  aov(Y ~ A + B + A*B)
		self.z       = 2.066, 0.654, 0.770
		self.df      = (2,90), (4,90), (8,90)
		self.p       = 0.133, 0.626, 0.630

class SPM1D4x4(_base.DatasetANOVA2):
	def _set_values(self):
		nA,nB,nSubj  = 4,4,20
		self.A       = np.array([0]*nSubj*nB + [1]*nSubj*nB + [2]*nSubj*nB + [3]*nSubj*nB)
		self.B       = np.array( list(range(nB)) *nSubj*nA)
		self.SUBJ    = np.array( np.sort( list(range(nSubj))*nB ).tolist() * nA )
		self.Y       = np.array([5, 1, 9, 1, 9, 5, 2, 0, 8, 9, 2, 8, 0, 9, 5, 7, 4, 2, 1, 8, 5, 4, 3, 3, 3, 4, 3, 3, 6, 5, 5, 2, 7, 3, 2, 8, 2, 6, 3, 9, 4, 0, 5, 0, 1, 4, 5, 1, 4, 1, 8, 3, 6, 2, 0, 1, 2, 6, 4, 9, 0, 2, 0, 3, 8, 2, 2, 1, 3, 7, 0, 6, 4, 8, 4, 2, 0, 3, 5, 3, 0, 4, 4, 9, 0, 0, 5, 6, 7, 0, 9, 6, 9, 1, 7, 8, 5, 6, 9, 9, 4, 6, 6, 9, 4, 3, 0, 0, 1, 4, 0, 5, 2, 7, 0, 9, 6, 2, 2, 4, 0, 9, 5, 5, 5, 5, 6, 8, 3, 5, 1, 8, 7, 1, 8, 5, 1, 9, 8, 4, 9, 2, 6, 7, 4, 8, 9, 1, 6, 7, 6, 5, 7, 2, 4, 1, 1, 1, 4, 4, 2, 8, 2, 6, 2, 9, 1, 3, 5, 1, 2, 4, 4, 5, 4, 0, 0, 2, 7, 6, 8, 1, 6, 6, 0, 4, 4, 5, 1, 6, 1, 0, 9, 5, 1, 5, 5, 6, 5, 6, 9, 1, 7, 5, 9, 4, 6, 8, 2, 0, 1, 3, 6, 9, 4, 7, 4, 1, 8, 1, 6, 6, 6, 2, 3, 9, 1, 5, 2, 8, 2, 8, 5, 4, 3, 0, 2, 1, 9, 8, 6, 7, 2, 4, 5, 5, 2, 1, 3, 3, 2, 1, 6, 2, 0, 9, 6, 0, 0, 4, 4, 5, 4, 7, 7, 5, 2, 1, 3, 3, 7, 3, 0, 6, 9, 7, 4, 9, 4, 4, 3, 2, 9, 4, 5, 1, 4, 0, 5, 7, 1, 1, 7, 7, 7, 7, 7, 0, 7, 6, 2, 3, 9, 6, 7, 3, 4, 6, 2, 0, 2, 0, 5, 1, 7, 1, 9, 6, 5, 4])
		#results computed using R (r-project.org):  aov(Y ~ A + B + A*B)
		self.z       = 1.143, 0.193, 0.772
		self.df      = (3,304), (3,304), (9,304)
		self.p       = 0.332, 0.901, 0.642
		self._rtol   = 0.01


class SPM1D4x5(_base.DatasetANOVA2):
	def _set_values(self):
		nA,nB,nSubj  = 4,5,10
		self.A       = np.array([0]*nSubj*nB + [1]*nSubj*nB + [2]*nSubj*nB + [3]*nSubj*nB)
		self.B       = np.array( list(range(nB)) *nSubj*nA)
		self.SUBJ    = np.array( np.sort( list(range(nSubj))*nB).tolist() * nA )
		self.Y       = np.array([9, 4, 6, 6, 4, 0, 7, 7, 1, 5, 7, 9, 2, 9, 8, 3, 3, 3, 0, 9, 8, 6, 2, 4, 2, 9, 1, 9, 3, 3, 7, 6, 1, 5, 5, 3, 6, 8, 5, 6, 7, 9, 4, 1, 5, 3, 1, 6, 6, 3, 3, 8, 5, 0, 9, 1, 4, 3, 4, 2, 2, 3, 3, 5, 4, 3, 9, 6, 1, 0, 5, 9, 4, 8, 6, 4, 2, 3, 3, 1, 6, 0, 4, 6, 2, 9, 2, 2, 6, 1, 6, 9, 6, 3, 3, 3, 5, 5, 9, 6, 6, 9, 7, 7, 3, 9, 9, 2, 0, 0, 6, 0, 4, 8, 5, 1, 1, 7, 0, 9, 0, 7, 0, 0, 6, 3, 9, 0, 7, 9, 0, 6, 1, 0, 7, 1, 7, 8, 0, 3, 2, 6, 3, 1, 4, 7, 6, 5, 8, 8, 1, 6, 5, 0, 9, 5, 9, 7, 2, 9, 5, 0, 4, 4, 8, 9, 8, 8, 7, 7, 6, 2, 0, 9, 9, 9, 2, 2, 1, 6, 1, 7, 5, 4, 7, 6, 9, 3, 9, 9, 6, 0, 5, 6, 8, 3, 9, 4, 5, 0])
		#results computed using R (r-project.org):  aov(Y ~ A + B + A*B)
		self.z       = 1.423, 1.616, 0.871
		self.df      = (3,180), (4,180), (12,180)
		self.p       = 0.238, 0.172, 0.577

