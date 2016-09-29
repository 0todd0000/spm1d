
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
		self.SUBJ   = np.sort( list(range(10))*6 )
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



class SPM1D3x3(_base.DatasetANOVA2rm):
	def _set_values(self):
		nSubj        = 5
		self.A       = np.array([0]*nSubj*3 + [1]*nSubj*3 + [2]*nSubj*3)
		self.B       = np.array([0,1,2]*nSubj*3)
		self.SUBJ    = np.array( list(range(nSubj))*3*3 )
		self.Y       = np.array([6, 2, 7, 1, 3, 5, 3, 4, 7, 7, 3, 5, 7, 9, 9, 0, 3, 1, 1, 9, 4, 7, 5, 0, 9, 4, 1, 8, 9, 6, 4, 5, 9, 8, 5, 3, 7, 3, 9, 1, 4, 5, 6, 4, 0])
		#results computed using R (r-project.org):  aov(Y ~ A + B + A*B + Error(SUBJ/(A*B) ))
		self.z       = 0.173, 0.048, 1.691
		self.df      = (2,8), (2,8), (4,16)
		self.p       = 0.844, 0.953, 0.201
		self._rtol   = 0.01

class SPM1D3x4(_base.DatasetANOVA2rm):
	def _set_values(self):
		nA,nB,nSubj  = 3,4,10
		self.A       = np.array([0]*nSubj*nB + [1]*nSubj*nB + [2]*nSubj*nB)
		self.B       = np.array(  list(range(nB))*nSubj*nA )
		self.SUBJ    = np.array( np.sort(range(nSubj)*nB).tolist() * nA )
		self.Y       = np.array([2, 2, 5, 5, 4, 8, 6, 5, 5, 5, 0, 0, 6, 1, 0, 3, 6, 5, 7, 9, 4, 6, 7, 5, 1, 7, 4, 3, 4, 8, 6, 7, 8, 2, 0, 2, 9, 5, 1, 3, 9, 2, 7, 8, 9, 7, 4, 2, 3, 0, 1, 5, 0, 0, 6, 3, 7, 5, 3, 0, 8, 3, 4, 6, 9, 6, 0, 5, 9, 8, 5, 1, 7, 2, 4, 7, 0, 7, 5, 1, 1, 1, 0, 4, 3, 7, 4, 6, 7, 5, 9, 2, 0, 2, 3, 9, 1, 4, 6, 5, 8, 7, 4, 1, 3, 1, 7, 0, 0, 7, 0, 6, 2, 4, 0, 0, 6, 1, 3, 5])
		#results computed using R (r-project.org):  aov(Y ~ A + B + A*B + Error(SUBJ/(A*B) ))
		self.z       = 1.1, 1.041, 0.659
		self.df      = (2,18), (3,27), (6,54)
		self.p       = 0.354, 0.390, 0.683

class SPM1D3x5(_base.DatasetANOVA2rm):
	def _set_values(self):
		nA,nB,nSubj  = 3,5,7
		self.A       = np.array([0]*nSubj*nB + [1]*nSubj*nB + [2]*nSubj*nB)
		self.B       = np.array(  list(range(nB))*nSubj*nA  )
		self.SUBJ    = np.array( np.sort(range(nSubj)*nB).tolist() * nA )
		self.Y       = np.array([2, 6, 5, 0, 5, 1, 1, 5, 4, 0, 8, 8, 4, 7, 3, 0, 4, 7, 5, 7, 1, 3, 2, 3, 7, 3, 3, 0, 8, 6, 9, 3, 0, 7, 6, 5, 8, 8, 3, 5, 2, 2, 2, 6, 8, 7, 9, 8, 4, 8, 2, 4, 3, 8, 7, 2, 0, 8, 9, 5, 9, 4, 8, 0, 0, 6, 6, 8, 6, 7, 1, 8, 4, 4, 7, 7, 2, 6, 9, 6, 1, 8, 2, 5, 0, 9, 8, 7, 9, 4, 7, 9, 6, 9, 4, 6, 4, 2, 1, 4, 0, 8, 1, 8, 8])
		#results computed using R (r-project.org):  aov(Y ~ A + B + A*B + Error(SUBJ/(A*B) ))
		self.z       = 1.632, 0.651, 0.816
		self.df      = (2,12), (4,24), (8,48)
		self.p       = 0.236, 0.632, 0.592

class SPM1D4x4(_base.DatasetANOVA2rm):
	def _set_values(self):
		nA,nB,nSubj  = 4,4,20
		self.A       = np.array([0]*nSubj*nB + [1]*nSubj*nB + [2]*nSubj*nB + [3]*nSubj*nB)
		self.B       = np.array(  list(range(nB))*nSubj*nA  )
		self.SUBJ    = np.array( np.sort(range(nSubj)*nB).tolist() * nA )
		self.Y       = np.array([5, 1, 9, 1, 9, 5, 2, 0, 8, 9, 2, 8, 0, 9, 5, 7, 4, 2, 1, 8, 5, 4, 3, 3, 3, 4, 3, 3, 6, 5, 5, 2, 7, 3, 2, 8, 2, 6, 3, 9, 4, 0, 5, 0, 1, 4, 5, 1, 4, 1, 8, 3, 6, 2, 0, 1, 2, 6, 4, 9, 0, 2, 0, 3, 8, 2, 2, 1, 3, 7, 0, 6, 4, 8, 4, 2, 0, 3, 5, 3, 0, 4, 4, 9, 0, 0, 5, 6, 7, 0, 9, 6, 9, 1, 7, 8, 5, 6, 9, 9, 4, 6, 6, 9, 4, 3, 0, 0, 1, 4, 0, 5, 2, 7, 0, 9, 6, 2, 2, 4, 0, 9, 5, 5, 5, 5, 6, 8, 3, 5, 1, 8, 7, 1, 8, 5, 1, 9, 8, 4, 9, 2, 6, 7, 4, 8, 9, 1, 6, 7, 6, 5, 7, 2, 4, 1, 1, 1, 4, 4, 2, 8, 2, 6, 2, 9, 1, 3, 5, 1, 2, 4, 4, 5, 4, 0, 0, 2, 7, 6, 8, 1, 6, 6, 0, 4, 4, 5, 1, 6, 1, 0, 9, 5, 1, 5, 5, 6, 5, 6, 9, 1, 7, 5, 9, 4, 6, 8, 2, 0, 1, 3, 6, 9, 4, 7, 4, 1, 8, 1, 6, 6, 6, 2, 3, 9, 1, 5, 2, 8, 2, 8, 5, 4, 3, 0, 2, 1, 9, 8, 6, 7, 2, 4, 5, 5, 2, 1, 3, 3, 2, 1, 6, 2, 0, 9, 6, 0, 0, 4, 4, 5, 4, 7, 7, 5, 2, 1, 3, 3, 7, 3, 0, 6, 9, 7, 4, 9, 4, 4, 3, 2, 9, 4, 5, 1, 4, 0, 5, 7, 1, 1, 7, 7, 7, 7, 7, 0, 7, 6, 2, 3, 9, 6, 7, 3, 4, 6, 2, 0, 2, 0, 5, 1, 7, 1, 9, 6, 5, 4])
		#results computed using R (r-project.org):  aov(Y ~ A + B + A*B + Error(SUBJ/(A*B) ))
		self.z       = 1.082, 0.249, 0.719
		self.df      = (3,57), (3,57), (9,171)
		self.p       = 0.364, 0.861, 0.691
		self._rtol   = 0.01

class SPM1D4x5(_base.DatasetANOVA2rm):
	def _set_values(self):
		nA,nB,nSubj  = 4,5,10
		self.A       = np.array([0]*nSubj*nB + [1]*nSubj*nB + [2]*nSubj*nB + [3]*nSubj*nB)
		self.B       = np.array(  list(range(nB))*nSubj*nA  )
		self.SUBJ    = np.array( np.sort(range(nSubj)*nB).tolist() * nA )
		self.Y       = np.array([9, 4, 6, 6, 4, 0, 7, 7, 1, 5, 7, 9, 2, 9, 8, 3, 3, 3, 0, 9, 8, 6, 2, 4, 2, 9, 1, 9, 3, 3, 7, 6, 1, 5, 5, 3, 6, 8, 5, 6, 7, 9, 4, 1, 5, 3, 1, 6, 6, 3, 3, 8, 5, 0, 9, 1, 4, 3, 4, 2, 2, 3, 3, 5, 4, 3, 9, 6, 1, 0, 5, 9, 4, 8, 6, 4, 2, 3, 3, 1, 6, 0, 4, 6, 2, 9, 2, 2, 6, 1, 6, 9, 6, 3, 3, 3, 5, 5, 9, 6, 6, 9, 7, 7, 3, 9, 9, 2, 0, 0, 6, 0, 4, 8, 5, 1, 1, 7, 0, 9, 0, 7, 0, 0, 6, 3, 9, 0, 7, 9, 0, 6, 1, 0, 7, 1, 7, 8, 0, 3, 2, 6, 3, 1, 4, 7, 6, 5, 8, 8, 1, 6, 5, 0, 9, 5, 9, 7, 2, 9, 5, 0, 4, 4, 8, 9, 8, 8, 7, 7, 6, 2, 0, 9, 9, 9, 2, 2, 1, 6, 1, 7, 5, 4, 7, 6, 9, 3, 9, 9, 6, 0, 5, 6, 8, 3, 9, 4, 5, 0])
		#results computed using R (r-project.org):  aov(Y ~ A + B + A*B + Error(SUBJ/(A*B) ))
		self.z       = 1.213, 1.823, 0.835
		self.df      = (3,27), (4,36), (12,108)
		self.p       = 0.324, 0.146, 0.615


