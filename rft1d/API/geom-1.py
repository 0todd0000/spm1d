import numpy as np
import power1d

x     = np.random.rand( 101 )
obj   = power1d.geom.from_array( x ) # Continuum1D object
obj.plot()

x     = np.random.rand( 5, 101 )
objs  = power1d.geom.from_array( x ) # list of Continuum1D objects
[obj.plot()  for obj in objs]