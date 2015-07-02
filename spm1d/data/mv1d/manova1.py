# coding: utf-8

import os
import numpy as np
from .. import _base




class Dorn2012(_base.DatasetMANOVA1, _base.Dataset1D):
	def _set_values(self):
		self.cite     = 'Dorn, T. W., Schache, A. G., & Pandy, M. G. (2012). Muscular strategy shift in human running: dependence of running speed on hip and ankle muscle performance. Journal of Experimental Biology, 215(11), 1944–1956. http://doi.org/10.1242/jeb.064527'
		self.www      = 'https://simtk.org/home/runningspeeds'
		self.datafile = os.path.join(_base.get_datafilepath(), 'Dorn2012.npz')
		self.note     = 'Note     ', 'Unpublished results'
		### load and parse data:
		Z             = np.load(self.datafile)
		Y,FOOT,SPEED  = Z['Y'], Z['FOOT'], Z['SPEED']
		Z.close()
		### choose one foot:
		Y,SPEED       = Y[FOOT==0], SPEED[FOOT==0]
		A,u           = np.zeros(SPEED.size), np.unique(SPEED)
		for i,uu in enumerate(u):
			A[SPEED==uu] = i
		self.Y        = Y
		self.A        = np.asarray(A, dtype=int)
		self.z        = None
		self.df       = None
		self.p        = None



