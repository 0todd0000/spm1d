
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
		self.z     = 18.4,35.94,6.48, 3.80,1.35,3.69, 2.23
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



class RS3tworm(_base.DatasetANOVA3tworm):
	def _set_values(self):
		self.www   = 'https://real-statistics.com/anova-repeated-measures/one-between-subjects-factor-two-within-subjects-factors/'
		self.Y     = np.array([
		                         0.6, 19.4, 17.8, 33.7, 16.2, 34.9, 11.4, 34.4,   #Group 1
		                        16.1, 16.0, 13.4, 29.3, 10.6, 27.7,  8.9, 41.6,
		                        12.9, 12.0, 11.5, 26.8, 16.1, 32.6,  1.3, 30.2,
		                        20.8, 23.9, 38.9, 38.7, 27.0, 39.3, 41.4, 47.7,
		                         9.2, 15.7,  9.4, 23.2,  7.7, 35.2,  6.6, 37.2,
		                         4.8, 19.5, 20.0, 29.5, 19.3, 35.3, 11.1, 40.1,
		                         2.0, 14.9, 15.4, 32.0, 13.1, 26.3, 10.9, 37.6,

		                         2.4,  4.9, 13.0,  6.0,  7.3, 11.6,  8.8, 24.8,   #Group 2
		                        28.0, 42.6, 19.4, 27.6, 24.2, 23.2, 20.0, 25.2,
		                        14.5, 31.4, 28.3, 34.9, 27.9, 11.4, 22.8, 13.6,
		                         1.6,  2.7,  7.8,  7.7,  6.4,  3.3,  5.3, 11.3,
		                        33.5, 19.6, 21.1, 31.0, 34.8, 32.8, 24.2, 24.0,
		                         0.2,  4.9,  5.9, 13.0,  5.8,  8.7,  6.7, 12.3,
		                        19.3, 11.3, 23.5, 23.8, 21.8, 15.7, 12.6, 12.7,

		                        25.0, 33.0, 27.4, 36.2, 28.3, 36.6, 27.1, 34.9,   #Group 3
		                         4.8, 24.8,  8.0, 29.8,  2.9, 34.2, 17.7, 35.2,
		                        23.1, 29.0, 28.5, 33.6, 17.9, 32.8, 11.0, 28.8,
		                        13.7, 25.6, 14.9, 28.4, 18.1, 34.3,  9.8, 28.0,
		                        31.5, 35.7, 27.5, 33.3, 24.5, 37.6, 23.9, 32.2,
		                        11.1, 13.2,  8.2, 28.7,  7.9, 43.3,  9.2, 31.1,
		                        11.4, 20.7, 11.5, 31.7,  6.4, 34.1, 11.8, 34.1,])
		self.A     = np.array( [0]*56 + [1]*56 + [2]*56 )        #Group (G1, G2, G3)
		self.B     = np.array( [0,0,1,1,2,2,3,3]*21 )            #Test (T1, T2, T3, T4)
		self.C     = np.array( [0,1]*84 )                        #Hand (Left, Right)
		self.SUBJ  = np.array( [[s]*8  for s in range(21)] ).flatten()
		self.z     = 1.993896,9.168953,98.242719,  3.211200,17.825533,6.066639,  4.178520
		self.df    = (2,18),(3,54),(1,18),   (6,54),(2,18),(3,54),   (6,54)
		self.p     = 0.165127, 0.000053, 0.0,   0.009049, 0.000054, 0.001232,   0.001605
		self._atol = 0.001

