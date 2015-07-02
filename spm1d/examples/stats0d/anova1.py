
import numpy as np
from scipy import stats
from matplotlib import pyplot
import spm1d




#(0) Example one-way (0D):
dataset = spm1d.data.uv0d.anova1.Cars()
# dataset = spm1d.data.uv0d.anova1.Sound()
# dataset = spm1d.data.uv0d.anova1.Southampton1()
# dataset = spm1d.data.uv0d.anova1.ConstructionUnequalSampleSizes()
# dataset = spm1d.data.uv0d.anova1.RSUnequalSampleSizes()
print dataset
y,A     = dataset.get_data()



#(1) Conduct ANOVA:
spmF  = spm1d.stats.anova1(y, A, equal_var=True)
spmFi   = spmF.inference(0.05)
print spmFi


#(2) Compare to scipy.stats result:
yy      = [y[A==u] for u in np.unique(A)]
f,p     = stats.f_oneway(*yy)
print 'scipy.stats result:\n   F = %.5f\n   p = %.5f' %(f,p)



#(3) Plot design:
pyplot.close('all')
design    = spm1d.stats.anova.designs.ANOVA1(A)
design.plot()
pyplot.show()