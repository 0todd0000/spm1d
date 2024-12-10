import numpy as np
from matplotlib import pyplot
import rft1d
weather = rft1d.data.weather()
y = weather['Atlantic']  # (15 x 365) numpy array
pyplot.plot(y.T)
pyplot.xlabel('Day')
pyplot.ylabel('Temperature')
pyplot.title('Unfiltered weather data (Atlantic region)')