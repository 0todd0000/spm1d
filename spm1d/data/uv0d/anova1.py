
import numpy as np
from .. import _base



class _BadOneLevel(_base.DatasetANOVA1):
	def _set_values(self):
		Y  = np.array( [] )
		self.Y     = np.array( [643, 469, 484] )
		self.A     = np.array( [0]*3 )
		self.expected_warning = False
		self.expected_class = ValueError

class _BadTwoLevels(_base.DatasetANOVA1):
	def _set_values(self):
		Y  = np.array( [] )
		self.Y     = np.array( [643, 469, 484, 655, 427, 456] )
		self.A     = np.hstack( [0]*3 + [1]*3 )
		self.expected_warning = True
		self.expected_class = UserWarning



class Cars(_base.DatasetANOVA1):
	def _set_values(self):
		self.www     = 'http://cba.ualr.edu/smartstat/topics/anova/example.pdf'
		Y  = np.array([
			[643, 469, 484],
			[655, 427, 456],
			[702, 525, 402],
		])
		self.Y     = Y.T.flatten()
		self.A     = np.hstack( [0]*3 + [1]*3 + [2]*3 )
		self.z     = 25.17
		self.df    = (2, 6)
		self.p     = 0.001207


class ConstructionUnequalSampleSizes(_base.DatasetANOVA1):
	def _set_values(self):
		self.www     = 'http://stackoverflow.com/questions/8320603/how-to-do-one-way-anova-in-r-with-unequal-sample-sizes'
		Y  = np.array([
			[34,25,27,31,26,34,21],
			[33,35,31,31,42,33],
			[17,30,30,26,32,28,26,29],
			[28,33,31,27,32,33,40],
		])
		self.Y     = np.hstack(Y)
		self.A     = np.hstack([[i]*len(yy) for i,yy in enumerate(Y)])
		self.z     = 3.4971
		self.df    = (3, 24)
		self.p     = 0.03098



class RSUnequalSampleSizes(_base.DatasetANOVA1):
	def _set_values(self):
		self.www     = 'http://www.real-statistics.com/one-way-analysis-of-variance-anova/unplanned-comparisons/anova-unequal-sample-sizes/'
		Y  = np.array([
			[3, 5, 6, 1, 5, 6, 4, 3, 7, 4, 5],
			[2, 4, 3, 5, 1, 5, 2, 3, 6, 2, 4, 1],
			[5, 8, 6, 4, 7, 8, 5, 6, 6],
			[4, 5, 3, 7, 6, 3, 2, 2, 4, 5],
		])
		self.Y     = np.hstack(Y)
		self.A     = np.hstack([[i]*len(yy) for i,yy in enumerate(Y)])
		self.z     = 5.864845
		self.df    = (3, 38)
		self.p     = 0.00215




class Sound(_base.DatasetANOVA1):
	def _set_values(self):
		self.www     = 'http://web.mst.edu/~psyworld/anovaexample.htm'
		Y  = np.array([
			[7, 4, 6, 8, 6, 6, 2, 9],
			[5, 5, 3, 4, 4, 7, 2, 2],
			[2, 4, 7, 1, 2, 1, 5, 5],
		]).T
		self.Y     = Y.T.flatten()
		self.A     = np.hstack( [0]*8 + [1]*8 + [2]*8 )
		self.z     = 3.59
		self.df    = (2, 21)
		self.p     = 0.0456    #calculated as:  scipy.stats.f.sf(3.59, 2, 21)
		self._rtol = 0.01


class Southampton1(_base.DatasetANOVA1):
	def _set_values(self):
		self.www     = 'http://www.southampton.ac.uk/~cpd/anovas/datasets/Doncaster&Davey%20-%20Model%201_1%20One%20factor.txt'
		self.Y       = np.array([4.5924, -0.5488, 6.1605, 2.3374, 5.1873, 3.3579, 6.3092, 3.2831, 7.3809, 9.2085, 13.1147, 15.2654, 12.4188, 14.3951, 8.5986, 3.4945, 21.3220, 25.0426, 22.6600, 24.1283, 16.5927, 10.2129, 9.8934, 10.0203])
		self.A       = np.array([1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3])
		self.z       = 17.08
		self.df      = (2, 21)
		self.p       = '<0.001'




