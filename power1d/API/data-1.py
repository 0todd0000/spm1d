from matplotlib import pyplot
import power1d

data = power1d.data.weather()   #load data dictionary
y    = data['Continental']   #extract one region
pyplot.plot(y.T, color="k")