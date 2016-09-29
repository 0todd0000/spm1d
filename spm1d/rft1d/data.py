
'''
Example datasets

Current datasets include:

	* Weather (Ramsay & Silverman, 2005)
'''

# Copyright (C) 2016  Todd Pataky

import os
import numpy as np
from scipy.io import loadmat



def weather():
	'''
	This dataset was made available by Prof. James O. Ramsay
	of McGill University. The dataset was download from:
	http://www.psych.mcgill.ca/misc/fda/downloads/FDAfuns/Matlab
	on 16 August 2014 (see the `./examples/weather` directory).
	
	No license was found with that dataset. Only "daily.m" and
	"daily.mat" from that dataset are redistributed here, on
	the condition that the original source be acknowledged.

	The dataset is described here:
	http://www.psych.mcgill.ca/misc/fda/ex-weather-a1.html
	and also in:
	Ramsay JO, Silverman BW (2005). Functional Data Analysis
	(Second Edition), Springer, New York.
	Chapter 13: "Modelling functional responses with
	multivariate covariates"
	
	Data subsets include:

	- 'Atlantic'
	- 'Pacific'
	- 'Continental'
	- 'Arctic'
	
	
	:Example use:
	
	>>> weather = rft1d.data.weather()
	>>> y = weather['Atlantic']  # (15 x 365) numpy array
	>>> from matplotlib import pyplot
	>>> pyplot.plot(y.T)
	'''
	fname    = os.path.join(os.path.dirname(__file__), 'data', 'weather', 'daily.mat')
	M        = loadmat(fname)
	Y        = M['tempav'].T
	geogind  = M['geogindex'].flatten()
	### place indices (from daily.m, Lines 412-415)
	atlindex = [1,2,4,8,9,13,14,15,19,22,23,24,25,28,34] #Atlantic
	pacindex = [12,17,18,30,31] #Pacific
	conindex = [3,5,6,7,16,20,26,27,29,32,33,35] #Continental
	artindex = [10,11,21] #Arctic
	### boolean indices for places:
	i0       = np.array([i in atlindex for i in geogind])
	i1       = np.array([i in pacindex for i in geogind])
	i2       = np.array([i in conindex for i in geogind])
	i3       = np.array([i in artindex for i in geogind])
	### extract places:
	y0       = Y[i0]
	y1       = Y[i1]
	y2       = Y[i2]
	y3       = Y[i3]
	### build dictionary:
	D        = dict(Atlantic=y0, Pacific=y1, Continental=y2, Arctic=y3)
	return D

