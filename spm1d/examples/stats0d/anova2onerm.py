
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
print dataset



#(1) Run ANOVA:
F = spm1d.stats.anova2onerm(y, A, B, SUBJ)
Fvalues = [f.z for f in F]
DF = [f.df for f in F]
print Fvalues
print DF



