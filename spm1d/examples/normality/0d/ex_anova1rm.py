
import numpy as np
import spm1d



#(0) Load dataset:
dataset  = spm1d.data.uv0d.anova1rm.Abdi2010()
dataset  = spm1d.data.uv0d.anova1rm.Groceries()
dataset  = spm1d.data.uv0d.anova1rm.Imacelebrity()
dataset  = spm1d.data.uv0d.anova1rm.Southampton1rm()
y,A,SUBJ = dataset.get_data()



#(1) Conduct normality test:
np.random.seed(0)
alpha      = 0.05
spmi       = spm1d.stats.normality.anova1rm(y, A, SUBJ).inference(alpha)
print( spmi )


