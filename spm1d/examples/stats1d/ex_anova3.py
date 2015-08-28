
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
FFi          = [F.inference(alpha)   for F in FF]


#(2) Plot results:
pyplot.close('all')
titles       = ['Main effect A',
               'Main effect B',
               'Main effect C',
               'Interaction AB',
               'Interaction AC',
               'Interaction BC',
               'Interaction ABC',
]
for i,Fi in enumerate(FFi):
	ax = pyplot.subplot(3,3,i+1)
	Fi.plot()
	ax.text(0.1, 0.85, titles[i], transform=ax.transAxes)
pyplot.show()





