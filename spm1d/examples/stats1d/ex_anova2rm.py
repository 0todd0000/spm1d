
import numpy as np
from matplotlib import pyplot
import spm1d



#(0) Load data:
dataset      = spm1d.data.uv1d.anova2rm._BadNoResiduals()
Y,A,B,SUBJ   = dataset.get_data()




#(1) Conduct ANOVA:
alpha        = 0.05
FF           = spm1d.stats.anova2rm(Y, A, B, SUBJ, equal_var=True)
FFi          = [F.inference(alpha, interp=False)  for F in FF]






