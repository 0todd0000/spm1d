
import numpy as np
from matplotlib import pyplot
import spm1d






#(0) Load data:
dataset   = spm1d.data.uv0d.anova3nested.SouthamptonNested3()
y,A,B,C   = dataset.get_data()
print dataset



#(1) Conduct ANOVA:
FF        = spm1d.stats.anova3nested(y, A, B, C, equal_var=False)
FFi       = [F.inference(0.05)  for F in FF]
fvalues   = [Fi.z  for Fi in FFi]
df        = [F.df  for F in FF]
pvalues   = [Fi.p  for Fi in FFi]
print 'Calculated results:'
print fvalues
print df
print pvalues



#(2) Plot design:
pyplot.close('all')
design    = spm1d.stats.anova.designs.ANOVA3(A, B, C)
design.plot()
pyplot.show()

