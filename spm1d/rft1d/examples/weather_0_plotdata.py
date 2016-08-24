
import numpy as np
from scipy.ndimage.filters import gaussian_filter1d
from matplotlib import pyplot
from spm1d import rft1d



#(0) Load weather data:
weather  = rft1d.data.weather() #dictionay containing geographical locations
### choose two geographical locations:
y0       = weather['Atlantic']
y1       = weather['Pacific']
y2       = weather['Continental']
y3       = weather['Arctic']
### smooth:
y0       = gaussian_filter1d(y0, 8.0, axis=1, mode='wrap')
y1       = gaussian_filter1d(y1, 8.0, axis=1, mode='wrap')
y2       = gaussian_filter1d(y2, 8.0, axis=1, mode='wrap')
y3       = gaussian_filter1d(y3, 8.0, axis=1, mode='wrap')




#(1) Plot:
pyplot.close('all')
labels = ['Atlantic', 'Pacific', 'Continental', 'Artic']
colors = ['r', 'g', 'b', 'k']
ax     = pyplot.axes()
for y,color,label in zip((y0,y1,y2,y3), colors, labels):
	h  = ax.plot(y.T, color=color)
	h[0].set_label(label)
ax.set_xlabel('Day', size=16)
ax.set_ylabel('Temperature', size=16)
ax.legend()
ax.set_title('Weather dataset (Ramsay et al. 2005)', size=20)
pyplot.show()










