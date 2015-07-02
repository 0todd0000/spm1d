
import numpy as np
from matplotlib import pyplot
import spm1d






#(0) Load data:
dataset      = spm1d.data.uv0d.anova3tworm.NYUHiringExperience()
# dataset      = spm1d.data.uv0d.anova3tworm.Southampton3tworm()
y,A,B,C,SUBJ = dataset.get_data()
print dataset




#(1) Conduct ANOVA:
FF        = spm1d.stats.anova3tworm(y, A, B, C, SUBJ)
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
design    = spm1d.stats.anova.designs.ANOVA3tworm(A, B, C, SUBJ)
design.plot()
pyplot.show()


