from matplotlib import pyplot
import rft1d
np.random.seed(3)
y = rft1d.randn1d(1, 101, 20.0, pad=True)
pyplot.figure(figsize=(5,3))
pyplot.plot(y, 'ko-')
pyplot.plot([0,100], [-0.2]*2, 'r--')
pyplot.xlim(0, 5)
pyplot.ylim(-0.3, 0.4)