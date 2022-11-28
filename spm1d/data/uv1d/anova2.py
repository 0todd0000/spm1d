# coding: utf-8

import os
import numpy as np
from .. import _base


class Besier2009kneeflexion(_base.DatasetANOVA2, _base.Dataset1D):
	def _set_values(self):
		self.cite     = 'Besier, T. F., Fredericson, M., Gold, G. E., Beaupré, G. S., & Delp, S. L. (2009). Knee muscle forces during walking and running in patellofemoral pain patients and pain-free controls. Journal of Biomechanics, 42(7), 898–905. http://doi.org/10.1016/j.jbiomech.2009.01.032'
		self.www      = 'https://simtk.org/home/muscleforces'
		self.datafile = os.path.join(_base.get_datafilepath(), 'Besier2009kneeflexion.npz')
		self.note     = 'Results  ', 'Pataky, T. C., Vanrenterghem, J., & Robinson, M. A. (2015). Two-way ANOVA for scalar trajectories, with experimental evidence of non-phasic interactions. Journal of Biomechanics, 48(1), 186–189. http://doi.org/10.1016/j.jbiomech.2014.10.013'
		### load and parse data:
		Z             = np.load(self.datafile)
		self.Y        = Z['Y']
		self.A        = Z['GROUP']   #0:controls, 1:PFP
		self.B        = Z['GENDER']  #0:female, 1:male
		Z.close()
		self.z        = None
		self.df       = None
		self.p        = None



class Dorn2012(_base.DatasetANOVA2, _base.Dataset1D):
	def _set_values(self):
		self.cite     = 'Dorn, T. W., Schache, A. G., & Pandy, M. G. (2012). Muscular strategy shift in human running: dependence of running speed on hip and ankle muscle performance. Journal of Experimental Biology, 215(11), 1944–1956. http://doi.org/10.1242/jeb.064527'
		self.www      = 'https://simtk.org/home/runningspeeds'
		self.datafile = os.path.join(_base.get_datafilepath(), 'Dorn2012.npz')
		### load and parse data:
		Z             = np.load(self.datafile)
		Y,A,B0        = Z['Y'], Z['FOOT'], Z['SPEED']
		Z.close()
		### choose one component:
		Y             = Y[:,:,1]
		B,uB          = np.zeros(B0.size), np.unique(B0)
		for i,u in enumerate(uB):
			B[B0==u]  = i
		B             = np.asarray(B, dtype=int)
		self.Y        = Y
		self.A        = A
		self.B        = B
		self.z        = None
		self.df       = None
		self.p        = None


class _SPM1D_ANOVA2_DATASET(_base.DatasetANOVA2, _base.Dataset1D):
	def _set_values(self):
		self._set_datafile()
		Z             = np.load(self.datafile)
		self.Y,self.A,self.B = Z['Y'], Z['A'], Z['B']
		Z.close()


class SPM1D_ANOVA2_2x2(_SPM1D_ANOVA2_DATASET):
	def _set_datafile(self):
		self.datafile = os.path.join(_base.get_datafilepath(), 'spm1d_anova2_2x2.npz')
class SPM1D_ANOVA2_2x3(_SPM1D_ANOVA2_DATASET):
	def _set_datafile(self):
		self.datafile = os.path.join(_base.get_datafilepath(), 'spm1d_anova2_2x3.npz')

class SPM1D_ANOVA2_3x3(_SPM1D_ANOVA2_DATASET):
	def _set_datafile(self):
		self.datafile = os.path.join(_base.get_datafilepath(), 'spm1d_anova2_3x3.npz')
class SPM1D_ANOVA2_3x4(_SPM1D_ANOVA2_DATASET):
	def _set_datafile(self):
		self.datafile = os.path.join(_base.get_datafilepath(), 'spm1d_anova2_3x4.npz')
class SPM1D_ANOVA2_3x5(_SPM1D_ANOVA2_DATASET):
	def _set_datafile(self):
		self.datafile = os.path.join(_base.get_datafilepath(), 'spm1d_anova2_3x5.npz')

class SPM1D_ANOVA2_4x4(_SPM1D_ANOVA2_DATASET):
	def _set_datafile(self):
		self.datafile = os.path.join(_base.get_datafilepath(), 'spm1d_anova2_4x4.npz')
class SPM1D_ANOVA2_4x5(_SPM1D_ANOVA2_DATASET):
	def _set_datafile(self):
		self.datafile = os.path.join(_base.get_datafilepath(), 'spm1d_anova2_4x5.npz')



