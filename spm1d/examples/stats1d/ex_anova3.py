
import numpy as np
from matplotlib import pyplot
import spm1d




#(0) Load data:
dataset      = spm1d.data.uv1d.anova3.SPM1D_ANOVA3_2x2x2()
# dataset      = spm1d.data.uv1d.anova3.SPM1D_ANOVA3_2x3x4()
Y,A,B,C      = dataset.get_data()



#(1) Conduct ANOVA:
alpha        = 0.05
FF           = spm1d.stats.anova3(Y, A, B, C, equal_var=True)
FFi          = FF.inference(0.05)
print( FFi )



#(2) Plot results:
pyplot.close('all')
for i,Fi in enumerate(FFi):
	ax = pyplot.subplot(3,3,i+1)
	Fi.plot()
	ax.text(0.1, 0.85, Fi.effect, transform=ax.transAxes)
pyplot.show()





