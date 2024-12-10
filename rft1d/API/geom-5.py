import power1d

obj = power1d.geom.ExponentialSaw(Q=101, x0=0.3, x1=3.6, rate=2.8, cutoff=85)
obj.plot()