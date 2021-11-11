
import numpy as np
import spm1d



#(0) Load dataset:
dataset      = spm1d.data.uv0d.anova3rm.SPM1D2x2x2()
# dataset      = spm1d.data.uv0d.anova3rm.SPM1D2x3x5()
# dataset      = spm1d.data.uv0d.anova3rm.SPM1D3x3x3()
y,A,B,C,SUBJ = dataset.get_data()
print( dataset )




#(1) Conduct non-parametric test:
np.random.seed(0)
alpha      = 0.05
snpmlist   = spm1d.stats.nonparam.anova3rm(y, A, B, C, SUBJ)
snpmilist  = snpmlist.inference(alpha, iterations=1000)
F,p        = np.array(   [(s.z, s.p)  for s in snpmilist]   ).T



#(1) Conduct non-parametric test:
np.random.seed(0)
alpha      = 0.05
snpmlist   = spm1d.stats.nonparam.anova3rm(y, A, B, C, SUBJ)
snpmilist  = snpmlist.inference(alpha, iterations=200)
print( 'Non-parametric results:')
print( snpmilist )



#(2) Compare to parametric test:
spmlist    = spm1d.stats.anova3rm(y, A, B, C, SUBJ, equal_var=True)
spmilist   = spmlist.inference(alpha)
print( 'Parametric results:')
print( spmilist )





