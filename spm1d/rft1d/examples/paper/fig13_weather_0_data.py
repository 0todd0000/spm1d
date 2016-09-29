
import numpy as np
from scipy.ndimage.filters import gaussian_filter1d
from matplotlib import pyplot
from spm1d import rft1d


### EPS production preliminaries:
fig_width_mm  = 100
fig_height_mm = 80
mm2in = 1/25.4
fig_width  = fig_width_mm*mm2in  	# width in inches
fig_height = fig_height_mm*mm2in    # height in inches
params = {	'backend':'ps', 'axes.labelsize':14,
			'font.size':12, 'text.usetex': False, 'legend.fontsize':12,
			'xtick.labelsize':8, 'ytick.labelsize':8,
			'font.family':'Times New Roman',  #Times
			'lines.linewidth':0.5,
			'patch.linewidth':0.25,
			'figure.figsize': [fig_width,fig_height]}
pyplot.rcParams.update(params)




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
ax     = pyplot.axes([0.13,0.15,0.84,0.83])
for y,color,label in zip((y0,y1,y2,y3), colors, labels):
	h  = ax.plot(y.T, color=color)
	h[0].set_label(label)
ax.legend(loc='lower center')
ax.set_xlabel('Day', size=16)
ax.set_ylabel('Temperature', size=16)
ax.set_ylim(-45, 25)
pyplot.show()



# pyplot.savefig('fig_weather_0_data.pdf')


