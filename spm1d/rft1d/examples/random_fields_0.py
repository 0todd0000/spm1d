
'''
Verbose random field generation.

Note:
When FWHM gets large (2FWHM>nNodes), the data should be padded prior to filtering.
Use **rft1d.random.randn1d** for optional padding.
'''



import numpy as np
from scipy.ndimage import gaussian_filter1d
from matplotlib import pyplot



#(0) Set parameters:
np.random.seed(12345)
nResponses = 5
nNodes     = 101
FWHM       = 20.0



#(1) Generate Gaussian 1D fields:
y          = np.random.randn(nResponses, nNodes)
#convolve with a Gaussian kernel:
sd         = FWHM / np.sqrt(8*np.log(2))
y          = gaussian_filter1d(y, sd, axis=1, mode='wrap')
#scale to unit variance:
'''
Restore filtered data to unit variance.
This code is modified from "randomtalk.m" by Matthew Brett (Oct 1999)
Downloaded from http://www.fil.ion.ucl.ac.uk/~wpenny/mbi/index.html on 1 Aug 2014
'''
### define Gaussian kernel
t          = np.arange(  -0.5*(nNodes-1) , 0.5*(nNodes-1)+1  )
gf         = np.exp(-(t**2) / (2*sd**2))
gf        /= gf.sum()
### expected variance for this kernel
AG         = np.fft.fft(gf)
Pag        = AG * np.conj(AG)  #power of the noise
COV        = np.real( np.fft.ifft(Pag) )
svar       = COV[0]
scale      = np.sqrt(1.0/svar)
### scale the data:
y         *= scale




#(2) Plot:
pyplot.close('all')
pyplot.plot(y.T)
pyplot.plot([0,100], [0,0], 'k:')
pyplot.xlabel('Field position', size=16)
pyplot.ylabel('z', size=20)
pyplot.title('Random (Gaussian) fields', size=20)
pyplot.show()
