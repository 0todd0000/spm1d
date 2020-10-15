import numpy as np
import power1d

value = np.random.rand( 101 )
obj   = power1d.geom.Continuum1D( value )
obj.plot()