
import numpy as np
from .. import _base




class RSRegression(_base.DatasetRegress):
	def _set_values(self):
		self.www  = 'http://www.real-statistics.com/regression/hypothesis-testing-significance-regression-line-slope/'
		self.x    = np.array([5, 23, 25, 48, 17, 8, 4, 26, 11, 19, 14, 35, 29, 4, 23])
		self.Y    = np.array([80, 78, 60, 53, 85, 84, 73, 79, 81, 75, 68, 72, 58, 92, 65])
		self.z    = -3.67092
		self.df   = 1,13
		self.p    = 0.002822
		self.r    = -0.71343


class ColumbiaHeadCircumference(_base.DatasetRegress):
	def _set_values(self):
		self.www  = 'http://www.stat.columbia.edu/~martin/W2024/R4.pdf'
		self.x    = np.array([27.75, 24.5, 25.5, 26, 25, 27.75, 26.5, 27, 26.75, 26.75, 27.5])
		self.Y    = np.array([17.5, 17.1, 17.1,17.3, 16.9, 17.6, 17.3, 17.5, 17.3, 17.5, 17.5])
		self.mu   = 0.3
		self.z    = 6.63
		self.df   = 1,9
		self.p    = 9.59e-5
		self.r    = 0.8301**0.5














