import power1d

data     = power1d.data.weather()  # load data
y        = data['Continental']     # extract one region
m        = y.mean( axis=0 )        # mean continuum

baseline = power1d.geom.Continuum1D( m )
baseline.plot()