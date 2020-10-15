from matplotlib import pyplot
import power1d

data     = power1d.data.weather()  # load data
y        = data['Continental']     # extract one region
m        = y.mean( axis=0 )        # mean continuum

# approximate the experimental value using a Gaussian pulse:
Q        = 365  # continuum size
g0       = power1d.geom.GaussianPulse( Q , q=200 , fwhm=190 , amp=40 )
g1       = power1d.geom.Constant( Q , amp=23 )
baseline = g0 - g1  # subtract the geometries

ax       = pyplot.axes()
ax.plot( m , label='Experimental mean', color='k')
baseline.plot( ax=ax, color='g', linewidth=3, label='Model' )
ax.legend()