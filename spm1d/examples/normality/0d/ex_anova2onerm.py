
import numpy as np
import spm1d



#(0) Load dataset:
dataset    = spm1d.data.uv0d.anova2onerm.Santa23()
dataset    = spm1d.data.uv0d.anova2onerm.Southampton2onerm()
dataset    = spm1d.data.uv0d.anova2onerm.RSXLDrug()
y,A,B,SUBJ = dataset.get_data()
print( dataset )






#(1) Conduct normality test:
np.random.seed(0)
alpha      = 0.05
spmi       = spm1d.stats.normality.anova2onerm(y, A, B, SUBJ).inference(alpha)
print( spmi )



