
import numpy as np
from matplotlib import pyplot
import spm1d



#(0) Load data:
dataset    = spm1d.data.uv0d.anova2nested.QIMacros()
dataset    = spm1d.data.uv0d.anova2nested.SouthamptonNested1()
y,A,B      = dataset.Y, dataset.A, dataset.B
# print dataset



#(1) Conduct ANOVA:
FF        = spm1d.stats.anova2nested(y, A, B, equal_var=True)
# FFi       = [F.inference(0.05)  for F in FF]
# fvalues   = [Fi.z  for Fi in FFi]
# df        = [F.df  for F in FF]
# pvalues   = [Fi.p  for Fi in FFi]
# print 'Calculated results:'
# print fvalues
# print df
# print pvalues
#
#
#
# #(2) Plot design:
# pyplot.close('all')
# design    = spm1d.stats.anova.designs.ANOVA2nested(A, B)
# design.plot()
# pyplot.show()
