

import numpy as np
from .. import _base





class NCSSBeforeAfter(_base.DatasetHotellingsPaired):
	def _set_values(self):
		self.www  = 'http://ncss.wpengine.netdna-cdn.com/wp-content/themes/ncss/pdf/Procedures/NCSS/Hotellings_One-Sample_T2.pdf'
		self.YA   = np.array([[36,34,30], [36,36,28], [41,32,29], [11,10,8], [17,15,13], [21,20,18], [36,33,30], [36,35,34], [37,33,28], [31,28,25]])
		self.YB   = np.array([[38,35,29], [38,37,27], [43,31,25], [14,11,10], [19,14,12], [24,25,17], [40,34,28], [41,36,30], [36,37,29], [31,25,26]])
		self.z    = 17.034
		self.df   = (3, 9)
		self.p    = 0.0483



class RSXLHotellingsPaired(_base.DatasetHotellingsPaired):
	def _set_values(self):
		self.www  = 'http://www.real-statistics.com/multivariate-statistics/hotellings-t-square-statistic/paired-sample-hotellings-t-square/'
		self.YA = np.array([
		[6, 8, 3, 5, 19],
		[6, 7, 3, 4, 9],
		[5, 7, 1, 4, 16],
		[10, 9, 8, 4, 4],
		[7, 9, 7, 6, 9],
		
		[6, 6, 3, 9, 17],
		[5, 8, 6, 7, 6],
		[3, 7, 3, 6, 16],
		[8, 8, 9, 3, 8],
		[8, 6, 5, 3, 13],
		
		[5, 9, 5, 4, 17],
		[8, 8, 2, 3, 5],
		[5, 8, 7, 5, 8],
		[4, 9, 10, 2, 16],
		[2, 9, 4, 10, 14],
		
		[7, 5, 8, 6, 15],
		[4, 8, 8, 2, 16],
		[5, 10, 9, 3, 11],
		[7, 7, 3, 7, 12],
		[1, 5, 2, 7, 17],
		
		[5, 6, 7, 7, 20],
		[4, 3, 1, 2, 15],
		[7, 9, 6, 6, 9],
		[4, 5, 2, 4, 12],
		[8, 9, 5, 7, 18],
		])
		
		self.YB = np.array([
		[8, 6, 5, 6, 10],
		[8, 6, 3, 6, 4],
		[7, 5, 6, 4, 17],
		[9, 8, 6, 3 ,4],
		[8, 5, 6, 8, 11],

		[8, 7, 4, 4, 13],
		[7, 3, 6, 3, 8],
		[6, 6, 5, 8, 14],
		[6, 9, 7, 5, 12],
		[7, 5, 9, 6, 11],

		[7, 5, 4, 6, 15],
		[5, 7, 4, 4 ,6],
		[6 ,4, 6, 4, 12],
		[8, 7, 8, 5, 12],
		[5, 6, 5, 7, 12],

		[10, 5, 7, 6, 6],
		[9, 6, 9, 5, 11],
		[8, 7, 10, 5, 5],
		[6, 2, 5, 3, 8],
		[5, 7, 5, 5, 8],

		[8, 4, 8, 8, 10],
		[3, 2, 4, 4, 15],
		[8, 6, 3, 6, 12],
		[5, 4, 6, 5, 9],
		[6, 3, 4, 8, 8],
		])
		self.z    = 53.9482
		self.df   = (5, 24)
		self.p    = 0.000133
