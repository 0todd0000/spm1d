
import numpy as np
from .. import _base





class SouthamptonNested3(_base.DatasetANOVA3nested):
	def _set_values(self):
		self.www     = 'http://www.southampton.ac.uk/~cpd/anovas/datasets/Doncaster&Davey%20-%20Model%202_2%20Three%20factor%20nested.txt'
		self.A       = np.array([1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3])
		self.B       = np.array([1, 1, 1, 1, 2, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2])
		self.C       = np.array([1, 1, 2, 2, 1, 1, 2, 2, 1, 1, 2, 2, 1, 1, 2, 2, 1, 1, 2, 2, 1, 1, 2, 2])
		self.Y       = np.array([4.5924, -0.5488, 6.1605, 2.3374, 5.1873, 3.3579, 6.3092, 3.2831, 7.3809, 9.2085, 13.1147, 15.2654, 12.4188, 14.3951, 8.5986, 3.4945, 21.3220, 25.0426, 22.6600, 24.1283, 16.5927, 10.2129, 9.8934, 10.0203])
		self.z       = 4.02, 5.24, 2.86
		self.df      = (2,3), (3,6), (6,12)
		self.p       = 0.142, 0.041, 0.057
		self._atol   = 0.005



