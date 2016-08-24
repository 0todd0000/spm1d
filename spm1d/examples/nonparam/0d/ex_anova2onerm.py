
import numpy as np
import spm1d



#(0) Load dataset:
dataset    = spm1d.data.uv0d.anova2onerm.Santa23()
dataset    = spm1d.data.uv0d.anova2onerm.Southampton2onerm()
# dataset    = spm1d.data.uv0d.anova2onerm.RSXLDrug()
# dataset    = spm1d.data.uv0d.anova2onerm.SPM1D3x3()
# dataset    = spm1d.data.uv0d.anova2onerm.SPM1D3x4()
# dataset    = spm1d.data.uv0d.anova2onerm.SPM1D3x4A()
# dataset    = spm1d.data.uv0d.anova2onerm.SPM1D3x5()
# dataset    = spm1d.data.uv0d.anova2onerm.SPM1D4x4()
# dataset    = spm1d.data.uv0d.anova2onerm.SPM1D4x5()
y,A,B,SUBJ = dataset.get_data()
print( dataset )



#(1) Conduct non-parametric test:
np.random.seed(0)
alpha      = 0.05
snpmlist   = spm1d.stats.nonparam.anova2onerm(y, A, B, SUBJ)
snpmilist  = snpmlist.inference(alpha, iterations=200)
print( 'Non-parametric results:')
print( snpmilist )



#(2) Compare to parametric test:
spmlist    = spm1d.stats.anova2onerm(y, A, B, SUBJ, equal_var=True)
spmilist   = spmlist.inference(alpha)
print( 'Parametric results:')
print( spmilist )




