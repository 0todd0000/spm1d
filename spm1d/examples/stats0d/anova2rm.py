
import numpy as np
from matplotlib import pyplot
import spm1d




#(0) Load data:
dataset    = spm1d.data.uv0d.anova2rm.Antidepressant()
# dataset    = spm1d.data.uv0d.anova2rm.RSXLTraining()
# dataset    = spm1d.data.uv0d.anova2rm.SocialNetworks()
# dataset = spm1d.data.uv0d.anova2rm.Southampton2rm()

y,A,B,SUBJ = dataset.get_data()
# print dataset




# (1) Conduct ANOVA:
FF        = spm1d.stats.anova2rm(y, A, B, SUBJ, equal_var=True)
FFi       = [F.inference(0.05)  for F in FF]
fvalues   = [F.z   for F in FF]
df        = [F.df  for F in FF]
pvalues   = [Fi.p  for Fi in FFi]
print 'Calculated results:'
print fvalues
print df
print pvalues



#(2) Plot design:
pyplot.close('all')
design    = spm1d.stats.anova.designs.ANOVA2rm(A, B, SUBJ)
design.plot()
pyplot.show()

