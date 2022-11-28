
import os
import numpy as np
from .. import _base



class _SPM1D_ANOVA2NESTED_DATASET(_base.DatasetANOVA2nested, _base.Dataset1D):
	def _set_values(self):
		self._set_datafile()
		Z             = np.load(self.datafile)
		self.Y,self.A,self.B = Z['Y'], Z['A'], Z['B']
		Z.close()


class SPM1D_ANOVA2NESTED_2x2(_SPM1D_ANOVA2NESTED_DATASET):
	def _set_datafile(self):
		self.datafile = os.path.join(_base.get_datafilepath(), 'spm1d_anova2nested_2x2.npz')
class SPM1D_ANOVA2NESTED_2x3(_SPM1D_ANOVA2NESTED_DATASET):
	def _set_datafile(self):
		self.datafile = os.path.join(_base.get_datafilepath(), 'spm1d_anova2nested_2x3.npz')

class SPM1D_ANOVA2NESTED_3x3(_SPM1D_ANOVA2NESTED_DATASET):
	def _set_datafile(self):
		self.datafile = os.path.join(_base.get_datafilepath(), 'spm1d_anova2nested_3x3.npz')
class SPM1D_ANOVA2NESTED_3x4(_SPM1D_ANOVA2NESTED_DATASET):
	def _set_datafile(self):
		self.datafile = os.path.join(_base.get_datafilepath(), 'spm1d_anova2nested_3x4.npz')
class SPM1D_ANOVA2NESTED_3x5(_SPM1D_ANOVA2NESTED_DATASET):
	def _set_datafile(self):
		self.datafile = os.path.join(_base.get_datafilepath(), 'spm1d_anova2nested_3x5.npz')

class SPM1D_ANOVA2NESTED_4x4(_SPM1D_ANOVA2NESTED_DATASET):
	def _set_datafile(self):
		self.datafile = os.path.join(_base.get_datafilepath(), 'spm1d_anova2nested_4x4.npz')
class SPM1D_ANOVA2NESTED_4x5(_SPM1D_ANOVA2NESTED_DATASET):
	def _set_datafile(self):
		self.datafile = os.path.join(_base.get_datafilepath(), 'spm1d_anova2nested_4x5.npz')