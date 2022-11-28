
import numpy as np
from .. import _base




class AnimalsInResearch(_base.DatasetCI2):
	def _set_values(self):
		self.www      = 'http://onlinestatbook.com/2/estimation/difference_means.html'
		self.datafile = 'http://onlinestatbook.com/2/case_studies/animal_research.html'
		self.YA       = np.array([5, 5, 5, 2, 3, 7, 7, 4, 7, 5, 7, 7, 5, 3, 5, 7, 7], dtype=float)
		self.YB       = np.array([3, 2, 3, 5, 6, 4, 7, 2, 6, 3, 3, 6, 5, 4, 1, 4, 2], dtype=float)
		self.alpha    = 0.05
		self.mu       = 0
		self.ci       = (0.29, 2.65)
		self.note     = 'Note     ', 'To access the original data visit the "data file" link and select "Show Data" from the bottom of the page.'





