
import numpy as np
import matplotlib.pyplot as plt
import spm1d



#(0) Load dataset:
dataset    = spm1d.data.uv1d.regress.SpeedGRF()
Y,x        = dataset.get_data()



#(0a) Create one-tailed region of interest(ROI):
roi        = np.array([0]*Y.shape[1])
roi[0:20]  = +1
roi[30:65] = -1




#(1) Conduct regression:
alpha      = 0.05
t          = spm1d.stats.regress(Y, x, roi=roi)
ti         = t.inference(alpha, two_tailed=False, interp=True)
print( ti )




#(2) Plot:
plt.close('all')
plt.figure(figsize=(7.5,5))
ax      = plt.axes()
ti.plot()
ti.plot_threshold_label(fontsize=8)
ti.plot_p_values(size=10)
ax.set_xlabel('Time (%)')
plt.show()


