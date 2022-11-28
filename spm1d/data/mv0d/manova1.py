

import numpy as np
from .. import _base



class AnimalDepression(_base.DatasetMANOVA1):
	'''
	NOTES:  chisq value and p value computed in MATLAB
	'''
	def _set_values(self):
		self.www  = 'http://www.pearsonhighered.com/assets/hip/gb/uploads/Mayers_IntroStatsSPSS_Ch14.pdf'
		A         = np.array([
		[36,80,50,73,48,67],
		[48,93,28,87,48,50],
		[61,53,44,80,87,67],
		[42,53,44,62,42,50],
		[55,87,48,87,42,56],
		[42,60,67,67,42,56],
		[48,60,67,40,36,50],
		[48,98,50,90,61,49],
		[53,67,44,60,61,60],
		[48,93,80,93,42,48],
		])
		yA     = A[:,[0,3]]  #dogs
		yB     = A[:,[1,4]]  #cats
		yC     = A[:,[2,5]]  #hamsters
		self.Y = np.vstack([yA,yB,yC])
		self.A = np.array([0]*10 + [1]*10 + [2]*10)
		self.z    = 23.8481     #computed in MATLAB using manova1
		self.df   = (1, 4)
		self.p    = 0.000085673  #computed in MATLAB using manova1




class Stevens2002(_base.DatasetMANOVA1):
	'''
	NOTE 1:  In the PDF file there's an error on page 5.
	The third response in the K2 group should be (6,7) and not (5,7).
	NOTE 2:  The X2 and p values reported in the PDF have rounding errors.
	'''
	def _set_values(self):
		self.www  = 'http://faculty.smu.edu/kyler/courses/7314/MANOVA.pdf'
		self.Y    = np.array([[2,3],[3,4],[5,4],[2,5],    [4,8],[5,6],[6,7],    [7,6],[8,7],[10,8],[9,5],[7,6]  ])
		self.A    = np.array([0]*4 + [1]*3 + [2]*5)
		# self.z    = 20.4987
		# self.p    = 0.0004271
		self.z    = 20.4983     #computed in MATLAB using manova1
		self.df   = (1, 4)
		self.p    = 0.00039807  #computed in MATLAB using manova1





