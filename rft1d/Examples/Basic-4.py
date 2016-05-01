from matplotlib import pyplot
import rft1d
np.random.seed(0)
y = rft1d.randn1d(5, 101, 25.0)
ymax = y.max(axis=1)
x = y.argmax(axis=1)
pyplot.figure(figsize=(5,3))
pyplot.plot(y.T, 'k')
pyplot.plot(x, ymax, 'ro')