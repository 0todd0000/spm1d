
import numpy as np
from .. import _base




class Antidepressant(_base.DatasetANOVA2rm):
	def _set_values(self):
		self.www    = 'http://www.pc.rhul.ac.uk/staff/J.Larsson/teaching/pdfs/repeatedmeasures.pdf'
		Y = np.array([
			[70, 60, 81, 52],
			[66, 52, 70, 40],
			[56, 41, 60, 31],
			[68, 59, 77, 49],
		])
		m,n    = Y.shape
		SUBJ   = np.array( [range(m)]*n ).T
		A      = np.array( [[0]*m, [0]*m, [1]*m, [1]*m] ).T
		B      = np.array( [[0]*m, [1]*m, [0]*m, [1]*m] ).T
		self.Y = Y.T.flatten()
		self.A = A.T.flatten()
		self.B = B.T.flatten()
		self.SUBJ = SUBJ.T.flatten()
		self.z      = 1.459, 530.842, 192.667
		self.df     = (1, 3), (1, 3), (1, 3)
		self.p      = 0.314, 0.000, 0.001
		





class RSXLTraining(_base.DatasetANOVA2rm):
	def _set_values(self):
		self.www    = 'http://www.real-statistics.com/anova-repeated-measures/two-within-subjects-factors/'
		self.Y      = np.array([13,12,17,18,30,34,  12,19,18,6,18,30,  17,19,24,21,31,32,  12,25,25,18,39,40,  19,27,19,18,28,27,  6,12,6,6,18,23,  17,18,30,24,36,38,  18,29,36,22,36,40,  23,30,24,18,38,32,  18,12,24,24,25,34])
		self.A      = np.array([0,0,0,1,1,1]*10)
		self.B      = np.hstack([0,1,2,0,1,2]*10)
		self.SUBJ   = np.sort(range(10)*6)
		self.z      = 33.85228, 26.95919, 12.63227
		self.df     = (1, 9), (2, 18), (2, 18)
		self.p      = 0.000254, 3.85e-6, 0.000373







class SocialNetworks(_base.DatasetANOVA2rm):
	def _set_values(self):
		self.www    = 'https://www.youtube.com/watch?v=GnDiiNmSQzU'
		Y = np.array([
			[7, 6, 7, 4],
			[8, 5, 8, 5],
			[7, 6, 7, 5],
			[6, 6, 8, 6],
			[7, 8, 6, 4],
			[8, 6, 5, 3],
			[9, 7, 3, 4],
			[10, 9, 7, 5],
			[10, 10, 8, 4],
			[5, 9, 4, 6],
			[6, 6, 6, 4],
			[7, 7, 5, 5],
			[6, 8, 7, 5],
			[8, 9, 9, 5],
			[6, 10, 10, 4],
			[4, 9, 10, 6],
			[5, 5, 8, 4],
			[6, 7, 7, 3],
			[9, 8, 8, 4],
			[6, 8, 9, 5],
			[7, 7, 7, 2],
		], dtype=float)
		m,n    = Y.shape
		SUBJ   = np.array( [range(m)]*n ).T
		A      = np.array( [[0]*m, [0]*m, [1]*m, [1]*m] ).T
		B      = np.array( [[0]*m, [1]*m, [0]*m, [1]*m] ).T
		self.Y = Y.T.flatten()
		self.A = A.T.flatten()
		self.B = B.T.flatten()
		self.SUBJ = SUBJ.T.flatten()
		self.z      = 16.731, 15.491, 21.891
		self.df     = (1, 20), (1, 20), (1, 20)
		self.p      = 0.001, 0.001, 0.000


class Southampton2rm(_base.DatasetANOVA2rm):
	def _set_values(self):
		self.www     = 'http://www.southampton.ac.uk/~cpd/anovas/datasets/Doncaster&Davey%20-%20Model%206_2%20Two%20factor%20repeated%20measures.txt'
		self.A       = np.array([1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3])
		self.B       = np.array([1, 1, 1, 1, 2, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2])
		self.SUBJ    = np.array([1, 2, 3, 4, 1, 2, 3, 4, 1, 2, 3, 4, 1, 2, 3, 4, 1, 2, 3, 4, 1, 2, 3, 4])
		self.Y       = np.array([4.5924, -0.5488, 6.1605, 2.3374, 5.1873, 3.3579, 6.3092, 3.2831, 7.3809, 9.2085, 13.1147, 15.2654, 12.4188, 14.3951, 8.5986, 3.4945, 21.3220, 25.0426, 22.6600, 24.1283, 16.5927, 10.2129, 9.8934, 10.0203])
		self.z       = 67.58, 4.13, 7.82
		self.df      = (2,6), (1,3), (2,6)
		self.p       = '<0.001', 0.135, 0.021 









