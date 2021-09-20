
import matplotlib.pyplot as plt
import spm1d




#(0) Load data:
dataset  = spm1d.data.uv1d.anova1.Weather()
Y,A      = dataset.get_data()
Y0,Y1    = Y[A==0], Y[A==2]  #Atlantic and Contintental


#(1) Run stats
t = spm1d.stats.ttest2(Y0, Y1)
ti = t.inference(0.05, circular=True)
print( ti )


#(2) Plot:
plt.close('all')
ti.plot()
ti.plot_p_values()
plt.tight_layout()
plt.show()



