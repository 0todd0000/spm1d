
import os
import numpy as np
from .. import _base





class _BadNoResiduals(_base.DatasetANOVA2rm):
	def _set_values(self):
		Y  = np.array( [] )
		self.Y     = np.random.randn(12, 101)
		self.A     = np.array( [0,0,0, 0,0,0, 1,1,1, 1,1,1] )
		self.B     = np.array( [0,0,0, 1,1,1,  0,0,0,  1,1,1] )
		self.SUBJ  = np.array( [0,1,2, 0,1,2, 0,1,2, 0,1,2]  )
		self.expected_warning = True
		self.expected_class = UserWarning
		
		


class _SPM1D_ANOVA2RM_DATASET(_base.DatasetANOVA2rm, _base.Dataset1D):
	def _set_values(self):
		self._set_datafile()
		Z             = np.load(self.datafile)
		self.Y,self.A,self.B,self.SUBJ = Z['Y'], Z['A'], Z['B'], Z['SUBJ']
		Z.close()


class SPM1D_ANOVA2RM_2x2(_SPM1D_ANOVA2RM_DATASET):
	def _set_datafile(self):
		self.datafile = os.path.join(_base.get_datafilepath(), 'spm1d_anova2rm_2x2.npz')
class SPM1D_ANOVA2RM_2x3(_SPM1D_ANOVA2RM_DATASET):
	def _set_datafile(self):
		self.datafile = os.path.join(_base.get_datafilepath(), 'spm1d_anova2rm_2x3.npz')

class SPM1D_ANOVA2RM_3x3(_SPM1D_ANOVA2RM_DATASET):
	def _set_datafile(self):
		self.datafile = os.path.join(_base.get_datafilepath(), 'spm1d_anova2rm_3x3.npz')
class SPM1D_ANOVA2RM_3x4(_SPM1D_ANOVA2RM_DATASET):
	def _set_datafile(self):
		self.datafile = os.path.join(_base.get_datafilepath(), 'spm1d_anova2rm_3x4.npz')
class SPM1D_ANOVA2RM_3x5(_SPM1D_ANOVA2RM_DATASET):
	def _set_datafile(self):
		self.datafile = os.path.join(_base.get_datafilepath(), 'spm1d_anova2rm_3x5.npz')

class SPM1D_ANOVA2RM_4x4(_SPM1D_ANOVA2RM_DATASET):
	def _set_datafile(self):
		self.datafile = os.path.join(_base.get_datafilepath(), 'spm1d_anova2rm_4x4.npz')
class SPM1D_ANOVA2RM_4x5(_SPM1D_ANOVA2RM_DATASET):
	def _set_datafile(self):
		self.datafile = os.path.join(_base.get_datafilepath(), 'spm1d_anova2rm_4x5.npz')