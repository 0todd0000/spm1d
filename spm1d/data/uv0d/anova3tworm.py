
import numpy as np
from .. import _base






class NYUHiringExperience(_base.DatasetANOVA3tworm):
	def _set_values(self):
		self.www   = 'http://www.psych.nyu.edu/cohen/three_way_ANOVA.pdf'
		### data: Table 22.4  (page 715)
		### results:  Table 22.5  (page 721)
		### repeated-measures factors:  B, C
		self.Y     = np.array([
            5.2, 5.8, 5.6, 4.4,   #low,below,female
            5.2, 6.0, 5.6, 5.8,   #low,below,male

            5.8, 6.4, 6.0, 7.0,   #low,average,female
            6.0, 5.2, 6.2, 6.8,   #low,average,male

            7.4, 7.6, 6.6, 7.8,   #low,above,female
            7.6, 8.0, 7.8, 6.4,   #low,above,male



            4.8, 5.4, 4.2, 4.6,   #moderate,below,female
            5.4, 4.8 ,5.2 ,6.0,   #moderate,below,male

            5.6 ,5.4, 5.0, 6.2,   #moderate,average,female
            6.0, 6.6, 5.8, 5.4,   #moderate,average,male

            6.4, 5.8, 7.6, 7.2,   #moderate,above,female
            7.0, 7.6, 6.8, 6.4,   #moderate,above,male



            4.4, 5.2, 3.6, 4.0,   #high,below,female
            5.8, 6.6, 6.4, 5.0,   #high,below,male

            6.0, 5.6, 6.2, 5.2,   #high,average,female
            7.0, 6.2, 7.8, 6.8,   #high,average,male

            7.0, 6.6, 5.2, 6.8,   #high,above,female
            5.6, 4.8, 6.4, 5.8,   #high,above,male
			])
		self.A     = np.array( [0]*4*2*3 + [1]*4*2*3 + [2]*4*2*3 )   #Experience (Low, Moderate, High)
		self.B     = np.array( ([0]*4*2 + [1]*4*2 + [2]*4*2) *3 )    #Attractiveness (Below, Average, Above)
		self.C     = np.array( ([0]*4 + [1]*4) *3*3 )                #Gender (Female, Male)
		SUBJ       = np.array( [1,2,3,4]*2*3 )
		self.SUBJ  = np.hstack([SUBJ, SUBJ+10, SUBJ+20])
		self.z     = 18.4,35.81,6.48, 3.92,1.35,3.69, 2.23
		self.df    = (2,9),(2,18),(1,9),  (4,18),(2,9),(2,18),  (4,18)
		self.p     = '<0.001', '<0.001', '<0.05',    '<0.05', '>0.05', '<0.05',  '>0.05'
		self._atol = 0.15




class Southampton3tworm(_base.DatasetANOVA3tworm):
	def _set_values(self):
		self.www     = 'http://www.southampton.ac.uk/~cpd/anovas/datasets/Doncaster&Davey%20-%20Model%206_5%20Three%20factor%20model%20with%20RM%20on%20two%20cross%20factors.txt'
		self.A       = np.array([1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3])
		self.B       = np.array([1, 1, 1, 1, 2, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2])
		self.C       = np.array([1, 1, 2, 2, 1, 1, 2, 2, 1, 1, 2, 2, 1, 1, 2, 2, 1, 1, 2, 2, 1, 1, 2, 2])
		# self.SUBJ    = np.array([1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2])
		# subj         = np.array([1, 2, 1, 2])
		# self.SUBJ    = np.hstack([subj, subj+10, subj+20, subj+30, subj+40, subj+50])
		subj         = np.array([1, 2, 1, 2, 1, 2, 1, 2])
		self.SUBJ    = np.hstack([subj, subj+10, subj+20])
		self.Y       = np.array([-3.8558, 4.4076, -4.1752, 1.4913, 5.9699, 5.2141, 9.1467, 5.8209, 9.4082, 6.0296, 15.3014, 12.1900, 6.9754, 14.3012, 10.4266, 2.3707, 19.1834, 18.3855, 23.3385, 21.9134, 16.4482, 11.6765, 17.9727, 15.1760])
		self.z       = 44.34, 0.01, 1.10,     5.21, 0.47, 1.04,    2.33
		self.df      = (2,3), (1,3), (1,3),   (2,3),(2,3),(1,3),  (2,3)
		self.p       = 0.006,0.921,0.371,   0.106,0.666,0.383,   0.245
		self._atol   = 0.005




