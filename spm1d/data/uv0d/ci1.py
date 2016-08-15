
import numpy as np
from .. import _base




class MinnesotaGeyerRate(_base.DatasetCI1):
	def _set_values(self):
		self.www      = 'http://www.stat.umn.edu/geyer/3011/examp/conf.html'
		self.datafile = 'http://www.stat.umn.edu/geyer/3011/mdata/chap16/eg16-01.dat'
		self.Y        = np.array([29, 27, 34, 40, 22, 28, 14, 35, 26, 35, 12, 30, 23, 18, 11, 22, 23, 33], dtype=float)
		self.alpha    = 0.05
		self.mu       = None
		self.ci       = (21.52709, 29.80625)
		self.note     = 'Note     ', 'From "Example 16.1" at the link above.'

class WebsterSleep(_base.DatasetCI1):
	def _set_values(self):
		self.www   = 'http://faculty.webster.edu/woolflm/ci.html'
		self.Y     = np.array([4.5, 22, 7, 14.5, 9, 9, 3.5, 8, 11, 7.5, 18, 20, 7.5, 9, 10.5, 15, 19, 2.5, 5, 9, 8.5, 14, 20, 8])
		self.alpha = 0.05
		self.mu    = None
		self.ci    = (8.50, 13.33)
		self.note  = 'Note     ', 'The expected CI may be slightly incorrect due to rounding errors.'



