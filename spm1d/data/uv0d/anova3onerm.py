
import numpy as np
from .. import _base






class NYUCaffeine(_base.DatasetANOVA3onerm):
	def _set_values(self):
		self.www   = 'http://www.psych.nyu.edu/cohen/three_way_ANOVA.pdf'
		### data: Table 22.2  (page 705)
		### results:  Table 22.3  (page 709)
		### repeated-measures factor:  C
		self.Y     = np.array([26,30,29,23,21,
		                       24,29,28,20,20,
							   24,25,27,20,20,

							   29,26,23,29,35,
							   28,23,24,30,33,
							   26,23,25,27,22,

							   29,24,23,31,29,
							   26,22,20,30,27,
							   26,23,17,30,25,


							   24,20,15,27,28,
							   22,18,16,25,27,
							   17,15,13,19,22,

							   27,29,34,23,25,
							   26,30,32,20,23,
							   33,17,25,18,20,

							   24,30,30,25,23,
							   25,27,31,24,21,
							   20,24,25,17,22,


							   17,19,22,11,15,
							   16,19,20,11,14,
							    9, 6,11, 7,10,

							   25,21,19,25,24,
							   16,13,12,18,19,
							   10, 9, 8,12,14,

							   23,29,28,20,21,
							   23,28,26,17,19,
							   20,23,23,12,17,


							   16,18,20,14,11,
							   14,17,18,12,10,
							    5, 6,10, 7, 7,

							   24,19,20,27,26,
							   15,11,11,19,17,
							   14, 8,15,17,10,

							   25,16,19,27,26,
							   23,16,18,26,24,
							   18,14,12,21,21])
		self.A     = np.array( [0]*5*9 + [1]*5*9 + [2]*5*9 + [3]*5*9 )    #Sleep deprivation (None, JetLag, Interrupt, Total)
		self.B     = np.array( ([0]*5*3 + [1]*5*3 + [2]*5*3) *4 )         #Stimulation (Placebo, Motivation, Caffeine)
		self.C     = np.array( ([0]*5 + [1]*5 + [2]*5) *3*4 )             #Time  (Day2, Day4, Day6)
		SUBJ       = np.array( [1,2,3,4,5]*3 + [6,7,8,9,10]*3 + [11,12,13,14,15]*3)
		self.SUBJ  = np.hstack([SUBJ, SUBJ+15, SUBJ+30, SUBJ+45])
		self.z     = 23.8,11.6,140.2,  1.65,6.28,5.58, 2.25
		self.df    = (3,48),(2,48),(2,96),   (6,48),(6,96),(4,96),   (12,96)
		self.p     = '<0.001', '<0.001', '<0.001',     '>0.05','<0.001','<0.001',  '<0.05',
		self._atol = 0.4





class Southampton3onerm(_base.DatasetANOVA3onerm):
	def _set_values(self):
		self.www     = 'http://www.southampton.ac.uk/~cpd/anovas/datasets/Doncaster&Davey%20-%20Model%206_7%20Three%20factor%20model%20with%20RM%20on%20a%20cross%20factor.txt'
		self.A       = np.array([1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3])
		self.B       = np.array([1, 1, 1, 1, 2, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2])
		self.C       = np.array([1, 1, 2, 2, 1, 1, 2, 2, 1, 1, 2, 2, 1, 1, 2, 2, 1, 1, 2, 2, 1, 1, 2, 2])
		subj         = np.array([1, 2, 1, 2])
		self.SUBJ    = np.hstack([subj, subj+10, subj+20, subj+30, subj+40, subj+50])
		self.Y       = np.array([-3.8558, 4.4076, -4.1752, 1.4913, 5.9699, 5.2141, 9.1467, 5.8209, 9.4082, 6.0296, 15.3014, 12.1900, 6.9754, 14.3012, 10.4266, 2.3707, 19.1834, 18.3855, 23.3385, 21.9134, 16.4482, 11.6765, 17.9727, 15.1760])
		self.z       = 34.42, 0.01, 1.11,     6.37, 0.47, 1.03,   2.30
		self.df      = (2,6),(1,6),(1,6),   (2,6),(2,6),(1,6),  (2,6)
		self.p       = 0.001,0.909,0.332,   0.033,0.645,0.350,   0.181
		self._atol   = 0.005

