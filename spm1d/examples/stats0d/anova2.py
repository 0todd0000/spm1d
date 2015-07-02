
import numpy as np
from matplotlib import pyplot
import spm1d





#(0) Load data:
dataset   = spm1d.data.uv0d.anova2.Mouse()       #2x2
dataset   = spm1d.data.uv0d.anova2.Detergent()     #2x3
dataset   = spm1d.data.uv0d.anova2.Satisfaction()  #2x3
dataset   = spm1d.data.uv0d.anova2.SouthamptonCrossed1()  #2x3
y,A,B     = dataset.get_data()
# print dataset




#(1) Conduct ANOVA:
FF        = spm1d.stats.anova2(y, A, B, equal_var=False)
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
design    = spm1d.stats.anova.designs.ANOVA2(A, B)
design.plot()
pyplot.show()
