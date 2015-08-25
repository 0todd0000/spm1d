

import numpy as np
from .. import _base


README  = 'No real datasets yet available.'


class _BadNoResiduals(_base.DatasetANOVA2rm):
	def _set_values(self):
		Y  = np.array( [] )
		self.Y     = np.random.randn(12, 101)
		self.A     = np.array( [0,0,0, 0,0,0, 1,1,1, 1,1,1] )
		self.B     = np.array( [0,0,0, 1,1,1,  0,0,0,  1,1,1] )
		self.SUBJ  = np.array( [0,1,2, 0,1,2, 0,1,2, 0,1,2]  )
		self.expected_warning = True
		self.expected_class = UserWarning