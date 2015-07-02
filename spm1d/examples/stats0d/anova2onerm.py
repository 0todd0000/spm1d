
import numpy as np
from matplotlib import pyplot
import spm1d




#(0) Load data:
dataset    = spm1d.data.uv0d.anova2onerm.Santa23()
# dataset    = spm1d.data.uv0d.anova2onerm.Southampton2onerm()
dataset    = spm1d.data.uv0d.anova2onerm.RSXLDrug()
y,A,B,SUBJ = dataset.Y, dataset.A, dataset.B, dataset.SUBJ
print dataset




#(1) Conduct ANOVA:
FF        = spm1d.stats.anova2onerm(y, A, B, SUBJ)
FFi       = [F.inference(0.05)  for F in FF]
fvalues   = [F.z   for F in FF]
df        = [F.df  for F in FF]
pvalues   = [Fi.p  for Fi in FFi]
print 'Calculated results:'
print fvalues
print df
print pvalues

# print FF



#(2) Plot design:
pyplot.close('all')
design    = spm1d.stats.anova.designs.ANOVA2onerm(A, B, SUBJ)
design.plot()
pyplot.show()


