
import numpy as np
import spm1d



#(0) Load dataset:
# dataset      = spm1d.data.uv0d.anova3onerm.NYUCaffeine()
dataset      = spm1d.data.uv0d.anova3onerm.Southampton3onerm()
y,A,B,C,SUBJ = dataset.get_data()
print( dataset )




#(1) Conduct non-parametric test:
np.random.seed(0)
alpha      = 0.05
snpmlist   = spm1d.stats.nonparam.anova3onerm(y, A, B, C, SUBJ)
snpmilist  = snpmlist.inference(alpha, iterations=500)
print( 'Non-parametric results:')
print( snpmilist )



#(2) Compare to parametric test:
spmlist    = spm1d.stats.anova3onerm(y, A, B, C, SUBJ, equal_var=True)
spmilist   = spmlist.inference(alpha)
print( 'Parametric results:')
print( spmilist )




