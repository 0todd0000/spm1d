
import spm1d





#(0) Load dataset:
dataset    = spm1d.data.uv0d.anova2onerm.Santa23UnequalSampleSizes()
dataset    = spm1d.data.uv0d.anova2onerm.Southampton2onermUnequalSampleSizes()
y,A,B,SUBJ = dataset.get_data()
print dataset



#(1) Run ANOVA:
F = spm1d.stats.anova2onerm(y, A, B, SUBJ)
Fvalues = [f.z for f in F]
DF = [f.df for f in F]
print Fvalues
print DF



