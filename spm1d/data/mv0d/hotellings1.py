

import numpy as np
from .. import _base




class RSXLHotellings1(_base.DatasetHotellings1):
	def _set_values(self):
		self.www  = 'http://www.real-statistics.com/multivariate-statistics/hotellings-t-square-statistic/one-sample-hotellings-t-square/'
		self.Y = np.array([
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
		self.mu   = np.array([7, 8, 5, 7, 9])
		self.z    = 52.6724
		self.df   = (5, 24)
		self.p    = 0.000155


class Sweat(_base.DatasetHotellings1):
	def _set_values(self):
		self.www  = 'http://www.public.iastate.edu/~maitra/stat501/lectures/InferenceForMeans-Hotelling.pdf'
		self.data = 'http://www.public.iastate.edu/~maitra/stat501/datasets/sweat.dat'
		Y = np.array([
		3.7, 48.5, 9.3,
		5.7, 65.1, 8.0,
		3.8, 47.2, 10.9,
		3.2, 53.2, 12.0,
		3.1, 55.5, 9.7,
		4.6, 36.1, 7.9,
		2.4, 24.8, 14.0,
		7.2, 33.1, 7.6,
		6.7, 47.4, 8.5,
		5.4, 54.1, 11.3,
		3.9, 36.9, 12.7,
		4.5, 58.8, 12.3,
		3.5, 27.8, 9.8,
		4.5, 40.2, 8.4,
		1.5, 13.5, 10.1,
		8.5, 56.4, 7.1,
		4.5, 71.6, 8.2,
		6.5, 52.8, 10.9,
		4.1, 44.1, 11.2,
		5.5, 40.9, 9.4
		])
		self.Y    = np.reshape(Y, (-1,3))
		self.mu   = np.array([4, 50, 10])
		self.z    = 9.74
		self.df   = (3, 19)
		self.p    = 0.06493



