
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





