
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
		s0          = np.sort(range(7)*5)
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
		subj0       = np.sort(range(6)*3)
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














