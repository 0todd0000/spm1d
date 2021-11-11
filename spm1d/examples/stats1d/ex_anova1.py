
import matplotlib.pyplot as plt
import spm1d



#(0) Load dataset:
dataset      = spm1d.data.uv1d.anova1.SpeedGRFcategorical()
dataset      = spm1d.data.uv1d.anova1.Weather()
Y,A          = dataset.get_data()



#(1) Run ANOVA:
alpha        = 0.05
F            = spm1d.stats.anova1(Y, A, equal_var=False)
Fi           = F.inference(alpha, interp=True, circular=False)
print( Fi )
### alternative syntax:
# Y0,Y1,Y2     = [Y[A==u] for u in np.unique(A)]
# F            = spm1d.stats.anova1((Y0,Y1,Y2), equal_var=False)


#(2) Plot results:
plt.close('all')
Fi.plot()
Fi.plot_threshold_label(bbox=dict(facecolor='w'))
# plt.ylim(-1, 500)
plt.xlabel('Time (%)', size=20)
plt.title(r'Critical threshold at $\alpha$=%.2f:  $F^*$=%.3f' %(alpha, Fi.zstar))
plt.show()





