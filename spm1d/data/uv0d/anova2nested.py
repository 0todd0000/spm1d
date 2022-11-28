
import numpy as np
from .. import _base





class QIMacros(_base.DatasetANOVA2nested):  #nested
	def _set_values(self):
		self.www   = 'https://www.qimacros.com/hypothesis-testing/anova-two-way-nested-excel/'
		self.Y     = np.array([3,4,7.1,7.1, 6,5,8.1,8.1, 3,4,7.1,9.1, 3,3,6,8.1,    1,2,5,9.9, 2,3,6,9.9, 2,4,5,8.9, 2,3,6,10.8])
		self.A     = np.array([0]*16 + [1]*16)
		self.B     = np.array([0,1,2,3]*4 + [4,5,6,7]*4)
		self.z     = 0.111, 45.726
		self.df    = (1, 6), (6, 24)
		self.p     = (0.742, 0.000)
		self._rtol = 0.01

class SouthamptonNested1(_base.DatasetANOVA2nested):
	def _set_values(self):
		self.www     = 'http://www.southampton.ac.uk/~cpd/anovas/datasets/Doncaster&Davey%20-%20Model%202_1%20Two%20factor%20nested.txt'
		self.A       = np.array([1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3])
		self.B       = np.array([1, 1, 1, 1, 2, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2])
		self.Y       = np.array([4.5924, -0.5488, 6.1605, 2.3374, 5.1873, 3.3579, 6.3092, 3.2831, 7.3809, 9.2085, 13.1147, 15.2654, 12.4188, 14.3951, 8.5986, 3.4945, 21.3220, 25.0426, 22.6600, 24.1283, 16.5927, 10.2129, 9.8934, 10.0203])
		self.z       = 4.02, 9.26
		self.df      = (2, 3), (3, 18)
		self.p       = (0.142, 0.001)




