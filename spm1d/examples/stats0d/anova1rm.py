
import numpy as np
from matplotlib import pyplot
import spm1d





#(0) Example one-way (0D):
dataset  = spm1d.data.uv0d.anova1rm.Abdi2010()
dataset  = spm1d.data.uv0d.anova1rm.Groceries()
dataset  = spm1d.data.uv0d.anova1rm.Imacelebrity()
dataset  = spm1d.data.uv0d.anova1rm.Southampton1rm()
y,A,SUBJ = dataset.get_data()
print dataset



#(1) Conduct ANOVA:
F        = spm1d.stats.anova1rm(y, A, SUBJ, equal_var=False)
Fi       = F.inference(0.05)
print Fi



#(2) Plot design:
pyplot.close('all')
design   = spm1d.stats.anova.designs.ANOVA1rm(A, SUBJ)
design.plot()
pyplot.show()

