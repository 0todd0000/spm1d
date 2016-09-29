import spm1d
dataset  = spm1d.data.uv1d.anova1.Weather()
Y,A      = dataset.get_data()
Y0,Y1    = Y[A==0], Y[A==2]  #Atlantic and Contintental regions
t        = spm1d.stats.ttest2(Y0, Y1)
ti       = t.inference(0.05, circular=True)
ti.plot()