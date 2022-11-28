
import numpy as np
from .. import _base




class RSXLDrug(_base.DatasetANOVA2onerm):
	def _set_values(self):
		self.design = 'Two-way repeated-measures ANOVA (with interaction) (one within-subject RM factor)'
		self.www    = 'http://www.real-statistics.com/anova-repeated-measures/one-between-subjects-factor-and-one-within-subjects-factor/'
		y0          = np.array([250,278,442,368,456,  65,207,341,382,298,  251,261,384,421,342,  241,314,423,415,468,  154,167,257,275,332,  103,286,401,291,367,  230,306,432,386,423])
		y1          = np.array([ 54,172,307,261,360,  20,116,425,398,268,   41,168,378,317,470,  200,157,283,259,273,   34, 86,351,280,320,   29, 81,193,240,233,    3, 54,285,216,245])
		y2          = np.array([118,124,365,311,331,  83,266,382,369,295,   38,207,289,385,373,   71,211,356,380,305,  123,331,407,461,445,   71,285,471,407,433,  108,247,317,307,324])
		a0,a1,a2    = [0]*y0.size, [1]*y1.size, [2]*y2.size
		b0          = [1,2,3,4,5]*7
		s0          = np.sort(  list( range(7) ) * 5  )
		self.Y      = np.hstack([y0,y1,y2])
		self.A      = np.hstack([a0,a1,a2])
		self.B      = np.hstack([b0]*3)
		self.SUBJ   = np.hstack([s0, s0+10, s0+20])
		self.z      = 8.301316, 114.6323, 2.164584
		self.df     = (2, 18), (4,72), (8,72)
		self.p      = 0.002789, 1.91e-30, 0.040346



class Santa23(_base.DatasetANOVA2onerm):
	def _set_values(self):
		self.design = 'Two-way repeated-measures ANOVA (with interaction) (one within-subject factor)'
		self.www    = 'http://www.statisticshell.com/docs/mixed.pdf'
		self.Y      = np.array([1,3,1, 2,5,3, 4,6,6, 5,7,4, 5,9,1, 6,9,3,     1,10,2, 4,8,1, 5,7,3, 4,9,2, 2,10,4, 5,10,2])
		self.A      = np.array([0]*18 + [1]*18)
		self.B      = np.hstack([0,1,2]*12)
		subj0       = np.sort(  list( range(6) ) * 3  )
		self.SUBJ   = np.hstack([subj0, subj0+10])
		self.z      = 0.511, 36.946, 3.856
		self.df     = (1,10), (2,20), (2, 20)
		self.p      = 0.491, 0.000, 0.038



class Southampton2onerm(_base.DatasetANOVA2onerm):
	def _set_values(self):
		self.www     = 'http://www.southampton.ac.uk/~cpd/anovas/datasets/Doncaster&Davey%20-%20Model%206_3%20Two%20factor%20model%20with%20RM%20on%20one%20cross%20factor.txt'
		self.A       = np.array([1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3])
		self.B       = np.array([1, 1, 1, 1, 2, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2])
		# self.SUBJ    = np.array([1, 2, 3, 4, 1, 2, 3, 4, 1, 2, 3, 4, 1, 2, 3, 4, 1, 2, 3, 4, 1, 2, 3, 4])
		subj         = np.array([1, 2, 3, 4, 1, 2, 3, 4])
		self.SUBJ    = np.hstack([subj, subj+10, subj+20])
		self.Y       = np.array([-3.8558, 4.4076, -4.1752, 1.4913, 5.9699, 5.2141, 9.1467, 5.8209, 9.4082, 6.0296, 15.3014, 12.1900, 6.9754, 14.3012, 10.4266, 2.3707, 19.1834, 18.3855, 23.3385, 21.9134, 16.4482, 11.6765, 17.9727, 15.1760])
		self.z       = 48.17, 0.01, 5.41
		self.df      = (2,9), (1,9), (2,9)
		self.p       = '<0.001', 0.915, 0.029
		self._atol   = 0.005





class SPM1D3x3(_base.DatasetANOVA2rm):
	def _set_values(self):
		nSubj        = 5
		self.A       = np.array([0]*nSubj*3 + [1]*nSubj*3 + [2]*nSubj*3)
		self.B       = np.array([0,1,2]*nSubj*3)
		self.SUBJ    = np.array( [(i*10 + np.arange(nSubj)).tolist() *3  for i in range(3)] ).flatten()
		self.Y       = np.array([6, 2, 7, 1, 3, 5, 3, 4, 7, 7, 3, 5, 7, 9, 9, 0, 3, 1, 1, 9, 4, 7, 5, 0, 9, 4, 1, 8, 9, 6, 4, 5, 9, 8, 5, 3, 7, 3, 9, 1, 4, 5, 6, 4, 0])
		#results computed using R (r-project.org):  aov(Y ~ A + B + A*B + Error(SUBJ/B ))
		self.z       = 0.204, 0.040, 1.832
		self.df      = (2,12), (2,24), (4,24)
		self.p       = 0.819, 0.961, 0.156
		self._rtol   = 0.01

class SPM1D3x4(_base.DatasetANOVA2rm):
	def _set_values(self):
		nA,nB,nSubj  = 3,4,10
		self.A       = np.array([0]*nSubj*nB + [1]*nSubj*nB + [2]*nSubj*nB)
		self.B       = np.array(  list( range(nB) ) * nSubj * nA  )
		self.SUBJ    = np.array( [np.sort( (i*10 + np.arange(nSubj)).tolist() *nB)  for i in range(nA)] ).flatten()
		self.Y       = np.array([2, 2, 5, 5, 4, 8, 6, 5, 5, 5, 0, 0, 6, 1, 0, 3, 6, 5, 7, 9, 4, 6, 7, 5, 1, 7, 4, 3, 4, 8, 6, 7, 8, 2, 0, 2, 9, 5, 1, 3, 9, 2, 7, 8, 9, 7, 4, 2, 3, 0, 1, 5, 0, 0, 6, 3, 7, 5, 3, 0, 8, 3, 4, 6, 9, 6, 0, 5, 9, 8, 5, 1, 7, 2, 4, 7, 0, 7, 5, 1, 1, 1, 0, 4, 3, 7, 4, 6, 7, 5, 9, 2, 0, 2, 3, 9, 1, 4, 6, 5, 8, 7, 4, 1, 3, 1, 7, 0, 0, 7, 0, 6, 2, 4, 0, 0, 6, 1, 3, 5])
		# self.Y       = np.array([41, 72, 48, 87, 27, 28, 12, 10, 32, 98, 71, 38,  9, 60, 13, 29, 56, 22, 64, 13, 17,  1, 71, 65, 20, 62, 71, 95, 57, 75, 31, 93, 58, 52, 88, 64, 78, 70, 23, 55, 96, 44, 21, 68, 16, 79, 83, 33, 69, 92, 77, 63, 30, 79, 62, 82, 41, 50, 15, 52, 14,  6, 51, 14, 50, 22, 55, 18, 16, 14, 11, 31, 57, 22, 76,  5, 16, 92, 44, 44, 77, 65, 71, 27, 69, 71, 66, 81, 81,  6, 78, 23, 38, 87, 69, 66, 64, 99, 75, 73, 52, 24, 12, 90,  8, 59, 18, 15, 71, 26, 45, 53, 21, 16, 13,  5, 23, 62, 89, 7])
		# #results computed using R (r-project.org):  aov(Y ~ A + B + A*B + Error(SUBJ/B ))
		self.z       = 1.013, 0.731, 0.757
		self.df      = (2,27), (3,81), (6,81)
		self.p       = 0.377, 0.536, 0.606

class SPM1D3x4A(_base.DatasetANOVA2rm):
	def _set_values(self):
		nA,nB,nSubj  = 3,4,5
		self.A       = np.array([0]*nSubj*nB + [1]*nSubj*nB + [2]*nSubj*nB)
		self.B       = np.array(  list( range(nB) ) * nSubj * nA  )
		self.SUBJ    = np.array( [np.sort( (i*10 + np.arange(nSubj)).tolist() *nB)  for i in range(nA)] ).flatten()
		self.Y       = np.array([7, 4, 8, 2, 8, 7, 9, 2, 2, 0, 1, 7, 7, 1, 7, 4, 3, 4, 2, 0, 3, 5, 9, 0, 8, 3, 2, 5, 8, 9, 3, 1, 7, 6, 7, 2, 3, 6, 5, 7, 1, 5, 8, 4, 9, 4, 9, 6, 8, 3, 9, 0, 2, 7, 5, 1, 8, 4, 2, 5])
		# #results computed using R (r-project.org):  aov(Y ~ A + B + A*B + Error(SUBJ/B ))
		self.z       = 0.517, 2.720, 0.321
		self.df      = (2,12), (3,36), (6,36)
		self.p       = 0.609, 0.0587, 0.9218


class SPM1D3x5(_base.DatasetANOVA2rm):
	def _set_values(self):
		nA,nB,nSubj  = 3,5,7
		self.A       = np.array([0]*nSubj*nB + [1]*nSubj*nB + [2]*nSubj*nB)
		self.B       = np.array(  list( range(nB) ) * nSubj * nA  )
		self.SUBJ    = np.array( [np.sort( (i*10 + np.arange(nSubj)).tolist() *nB)  for i in range(nA)] ).flatten()
		self.Y       = np.array([2, 6, 5, 0, 5, 1, 1, 5, 4, 0, 8, 8, 4, 7, 3, 0, 4, 7, 5, 7, 1, 3, 2, 3, 7, 3, 3, 0, 8, 6, 9, 3, 0, 7, 6, 5, 8, 8, 3, 5, 2, 2, 2, 6, 8, 7, 9, 8, 4, 8, 2, 4, 3, 8, 7, 2, 0, 8, 9, 5, 9, 4, 8, 0, 0, 6, 6, 8, 6, 7, 1, 8, 4, 4, 7, 7, 2, 6, 9, 6, 1, 8, 2, 5, 0, 9, 8, 7, 9, 4, 7, 9, 6, 9, 4, 6, 4, 2, 1, 4, 0, 8, 1, 8, 8])
		#results computed using R (r-project.org):  aov(Y ~ A + B + A*B + Error(SUBJ/B ))
		self.z       = 1.806, 0.678, 0.799
		self.df      = (2,18), (4,72), (8,72)
		self.p       = 0.193, 0.609, 0.606

class SPM1D4x4(_base.DatasetANOVA2rm):
	def _set_values(self):
		nA,nB,nSubj  = 4,4,20
		self.A       = np.array([0]*nSubj*nB + [1]*nSubj*nB + [2]*nSubj*nB + [3]*nSubj*nB)
		self.B       = np.array(  list( range(nB) ) * nSubj * nA  )
		subj         = np.array( np.sort(  list( range(nSubj) ) * nB  )  )
		self.SUBJ    = np.hstack(  [ (i*nSubj)+subj  for i in range(nA)] )
		self.Y       = np.array([5, 1, 9, 1, 9, 5, 2, 0, 8, 9, 2, 8, 0, 9, 5, 7, 4, 2, 1, 8, 5, 4, 3, 3, 3, 4, 3, 3, 6, 5, 5, 2, 7, 3, 2, 8, 2, 6, 3, 9, 4, 0, 5, 0, 1, 4, 5, 1, 4, 1, 8, 3, 6, 2, 0, 1, 2, 6, 4, 9, 0, 2, 0, 3, 8, 2, 2, 1, 3, 7, 0, 6, 4, 8, 4, 2, 0, 3, 5, 3, 0, 4, 4, 9, 0, 0, 5, 6, 7, 0, 9, 6, 9, 1, 7, 8, 5, 6, 9, 9, 4, 6, 6, 9, 4, 3, 0, 0, 1, 4, 0, 5, 2, 7, 0, 9, 6, 2, 2, 4, 0, 9, 5, 5, 5, 5, 6, 8, 3, 5, 1, 8, 7, 1, 8, 5, 1, 9, 8, 4, 9, 2, 6, 7, 4, 8, 9, 1, 6, 7, 6, 5, 7, 2, 4, 1, 1, 1, 4, 4, 2, 8, 2, 6, 2, 9, 1, 3, 5, 1, 2, 4, 4, 5, 4, 0, 0, 2, 7, 6, 8, 1, 6, 6, 0, 4, 4, 5, 1, 6, 1, 0, 9, 5, 1, 5, 5, 6, 5, 6, 9, 1, 7, 5, 9, 4, 6, 8, 2, 0, 1, 3, 6, 9, 4, 7, 4, 1, 8, 1, 6, 6, 6, 2, 3, 9, 1, 5, 2, 8, 2, 8, 5, 4, 3, 0, 2, 1, 9, 8, 6, 7, 2, 4, 5, 5, 2, 1, 3, 3, 2, 1, 6, 2, 0, 9, 6, 0, 0, 4, 4, 5, 4, 7, 7, 5, 2, 1, 3, 3, 7, 3, 0, 6, 9, 7, 4, 9, 4, 4, 3, 2, 9, 4, 5, 1, 4, 0, 5, 7, 1, 1, 7, 7, 7, 7, 7, 0, 7, 6, 2, 3, 9, 6, 7, 3, 4, 6, 2, 0, 2, 0, 5, 1, 7, 1, 9, 6, 5, 4])
		#results computed using R (r-project.org):  aov(Y ~ A + B + A*B + Error(SUBJ/B ))
		self.z       = 1.139, 0.193, 0.773
		self.df      = (3,76), (3,228), (9,228)
		self.p       = 0.339, 0.901, 0.641

class SPM1D4x5(_base.DatasetANOVA2rm):
	def _set_values(self):
		nA,nB,nSubj  = 4,5,10
		self.A       = np.array([0]*nSubj*nB + [1]*nSubj*nB + [2]*nSubj*nB + [3]*nSubj*nB)
		self.B       = np.array(  list( range(nB) ) * nSubj * nA  )
		subj         = np.array( np.sort(  list(range(nSubj)) *nB ) )
		self.SUBJ    = np.hstack(  [ (i*nSubj)+subj  for i in range(nA)])
		self.Y       = np.array([9, 4, 6, 6, 4, 0, 7, 7, 1, 5, 7, 9, 2, 9, 8, 3, 3, 3, 0, 9, 8, 6, 2, 4, 2, 9, 1, 9, 3, 3, 7, 6, 1, 5, 5, 3, 6, 8, 5, 6, 7, 9, 4, 1, 5, 3, 1, 6, 6, 3, 3, 8, 5, 0, 9, 1, 4, 3, 4, 2, 2, 3, 3, 5, 4, 3, 9, 6, 1, 0, 5, 9, 4, 8, 6, 4, 2, 3, 3, 1, 6, 0, 4, 6, 2, 9, 2, 2, 6, 1, 6, 9, 6, 3, 3, 3, 5, 5, 9, 6, 6, 9, 7, 7, 3, 9, 9, 2, 0, 0, 6, 0, 4, 8, 5, 1, 1, 7, 0, 9, 0, 7, 0, 0, 6, 3, 9, 0, 7, 9, 0, 6, 1, 0, 7, 1, 7, 8, 0, 3, 2, 6, 3, 1, 4, 7, 6, 5, 8, 8, 1, 6, 5, 0, 9, 5, 9, 7, 2, 9, 5, 0, 4, 4, 8, 9, 8, 8, 7, 7, 6, 2, 0, 9, 9, 9, 2, 2, 1, 6, 1, 7, 5, 4, 7, 6, 9, 3, 9, 9, 6, 0, 5, 6, 8, 3, 9, 4, 5, 0])
		#results computed using R (r-project.org):  aov(Y ~ A + B + A*B + Error(SUBJ/B ))
		self.z       = 1.447, 1.609, 0.868
		self.df      = (3,36), (4,144), (12,144)
		self.p       = 0.146, 0.267, 0.635






class Santa23UnequalSampleSizes(_base.DatasetANOVA2onerm):
	'''
	This is a minor modification of the Santa23 dataset to test unequal sample sizes.
	'''
	def _set_values(self):
		self.design = 'Two-way repeated-measures ANOVA (with interaction) (one within-subject factor)'
		self.www    = 'http://www.statisticshell.com/docs/mixed.pdf'
		self.Y      = np.array([1,3,1, 2,5,3, 4,6,6, 5,7,4, 5,9,1, 6,9,3,     1,10,2, 4,8,1, 5,7,3, 4,9,2, 2,10,4, 5,10,2,     3,4,5,  8,4,5,  10,9,9,  3,5,6,  4,5,8,  7,7,7])
		self.A      = np.array([0]*18 + [1]*(18+18))
		self.B      = np.hstack([0,1,2]*18)
		self.SUBJ   = np.array([0,  0,  0,  1,  1,  1,  2,  2,  2,  3,  3,  3,  4,  4,  4,  5,  5, 5,
                      10, 10, 10, 11, 11, 11, 12, 12, 12, 13, 13, 13, 14, 14, 14, 15, 15, 15,      16,16,16,   17,17,17,   18,18,18,   19,19,19,   20,20,20,   21,21,21])
		self.z       = 1.955, 9.763, 0.116
		self.df      = (1,16), (2,32), (2,32)
		self.p       = 0.181, 0.00049, 0.89069
		self._atol   = 0.005


class Southampton2onermUnequalSampleSizes(_base.DatasetANOVA2onerm):
	'''
	This is a minor modification of the Southampton2onerm dataset to test unequal sample sizes.
	'''
	def _set_values(self):
		self.www     = 'http://www.southampton.ac.uk/~cpd/anovas/datasets/Doncaster&Davey%20-%20Model%206_3%20Two%20factor%20model%20with%20RM%20on%20one%20cross%20factor.txt'
		self.A       = np.array([1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3])
		self.B       = np.array([1, 1, 1, 1, 2, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2, 1, 1, 2, 2])
		self.SUBJ    = np.array([1,  2,  3,  4,  1,  2,  3,  4, 11, 12, 13, 14, 11, 12, 13, 14, 21, 22, 23, 24, 21, 22, 23, 24, 25, 26, 25, 26])
		self.Y       = np.array([-3.8558, 4.4076, -4.1752, 1.4913, 5.9699, 5.2141, 9.1467, 5.8209, 9.4082, 6.0296, 15.3014, 12.1900, 6.9754, 14.3012, 10.4266, 2.3707, 19.1834, 18.3855, 23.3385, 21.9134, 16.4482, 11.6765, 17.9727, 15.1760, 15.0, 12.0, 16.0, 13.0])
		self.z       = 36.73, 0.000, 4.674
		self.df      = (2,11), (1,11), (2,11)
		self.p       = 1.35e-5, 0.9955, 0.0339
		self._atol   = 0.005
