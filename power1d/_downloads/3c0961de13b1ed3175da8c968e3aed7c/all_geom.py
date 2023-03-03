
import numpy as np
from matplotlib import pyplot
import power1d





#(0) Construct geom:
np.random.seed(0)
Q          = 101
geom = []
geom.append(   power1d.geom.Continuum1D( np.random.randn(Q) )   )
geom.append(   power1d.geom.Constant(Q, 1.3)   )
geom.append(   power1d.geom.Exponential(Q, x0=1.2, x1=3.2, rate=5)   )
geom.append(   power1d.geom.ExponentialSaw(Q, x0=0, x1=2.5, rate=10, cutoff=65)   )
geom.append(   power1d.geom.GaussianPulse(Q, q=60, sigma=None, fwhm=20, amp=3.2)   )
geom.append(   power1d.geom.Linear(Q, x0=0, x1=2.5, slope=None)   )
geom.append(   power1d.geom.Null(Q)   )
geom.append(   power1d.geom.SawPulse(Q, q0=50, q1=80, x0=0, x1=2.5)   )
geom.append(   power1d.geom.SawTooth(Q, q0=3, q1=13, x0=0, x1=2.5, dq=3)   )
geom.append(   power1d.geom.Sigmoid(Q, q0=40, q1=80, x0=0.6, x1=-2.7)   )
geom.append(   power1d.geom.Sinusoid(Q, q0=0, amp=1, hz=2)   )
geom.append(   power1d.geom.SquarePulse(Q, q0=40, q1=65, x0=0.3, x1=2.7)   )
geom.append(   power1d.geom.SquareTooth(Q, q0=5, q1=18, x0=1.2, x1=5.7, dq=8)   )
geom.append(   power1d.geom.TrianglePulse(Q, q0=60, q1=85, x0=1, x1=5)   )
geom.append(   power1d.geom.TriangleTooth(Q, q0=20, q1=35, x0=1, x1=5, dq=10)   )



#(1) Plot:
pyplot.figure(figsize=(16,7))
for i,p in enumerate(geom):
	ax = pyplot.subplot(3, 5, i+1)
	p.plot(ax)
	ax.text(0.05, 0.9, '%s' %p.__class__.__name__, transform=ax.transAxes, bbox=dict(facecolor='w', alpha=0.8), size=12)
pyplot.suptitle('All power1d.geom types', size=20)
# pyplot.show()




