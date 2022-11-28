
import os
import numpy as np
from .. import _base




class _SPM1D_ANOVA3NESTED_DATASET(_base.DatasetANOVA3nested, _base.Dataset1D):
	def _set_values(self):
		self._set_datafile()
		Z             = np.load(self.datafile)
		self.Y,self.A,self.B,self.C = Z['Y'], Z['A'], Z['B'], Z['C']
		Z.close()


class SPM1D_ANOVA3NESTED_2x2x2(_SPM1D_ANOVA3NESTED_DATASET):
	def _set_datafile(self):
		self.datafile = os.path.join(_base.get_datafilepath(), 'spm1d_anova3nested_2x2x2.npz')
class SPM1D_ANOVA3NESTED_2x4x2(_SPM1D_ANOVA3NESTED_DATASET):
	def _set_datafile(self):
		self.datafile = os.path.join(_base.get_datafilepath(), 'spm1d_anova3nested_2x4x2.npz')

