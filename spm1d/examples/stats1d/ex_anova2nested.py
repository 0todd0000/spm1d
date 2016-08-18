
import numpy as np
from matplotlib import pyplot
import spm1d




#(0) Load data:
dataset      = spm1d.data.uv1d.anova2nested.SPM1D_ANOVA2NESTED_2x2()
# dataset      = spm1d.data.uv1d.anova2nested.SPM1D_ANOVA2NESTED_2x3()
# dataset      = spm1d.data.uv1d.anova2nested.SPM1D_ANOVA2NESTED_3x3()
# dataset      = spm1d.data.uv1d.anova2nested.SPM1D_ANOVA2NESTED_3x4()
# dataset      = spm1d.data.uv1d.anova2nested.SPM1D_ANOVA2NESTED_3x5()
# dataset      = spm1d.data.uv1d.anova2nested.SPM1D_ANOVA2NESTED_4x4()
# dataset      = spm1d.data.uv1d.anova2nested.SPM1D_ANOVA2NESTED_4x5()
Y,A,B        = dataset.get_data()



#(1) Conduct ANOVA:
alpha        = 0.05
FF           = spm1d.stats.anova2nested(Y, A, B, equal_var=True)
FFi          = FF.inference(0.05)
print( FFi )


#(2) Plot results:
pyplot.close('all')
pyplot.subplot(221);  FFi[0].plot();  pyplot.title( FFi[0].effect )
pyplot.subplot(222);  FFi[1].plot();  pyplot.title( FFi[1].effect )
pyplot.show()





