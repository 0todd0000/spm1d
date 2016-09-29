
import numpy as np
from .. import _base




class RSWeightReduction(_base.DatasetT1):
	def _set_values(self):
		self.www  = 'http://www.real-statistics.com/students-t-distribution/one-sample-t-test/'
		self.Y    = np.array([23, 15, -5, 7, 1, -10, 12, -8, 20, 8, -2, -5])
		self.mu   = 0
		self.two_tailed = False
		self.z    = 1.449255
		self.df   = 1,11
		self.p    = 0.087585


class ColumbiaSalmonella(_base.DatasetT1):
	def _set_values(self):
		self.www  = 'http://www.stat.columbia.edu/~martin/W2024/R2.pdf'
		self.Y    = np.array([0.593, 0.142, 0.329, 0.691, 0.231, 0.793, 0.519, 0.392, 0.418])
		self.mu   = 0.3
		self.two_tailed = False
		self.z    = 2.2051
		self.df   = 1,8
		self.p    = 0.02927
	
	
	











