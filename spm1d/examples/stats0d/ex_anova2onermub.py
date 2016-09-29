
import spm1d





#(0) Load dataset:
dataset    = spm1d.data.uv0d.anova2onerm.Santa23UnequalSampleSizes()
dataset    = spm1d.data.uv0d.anova2onerm.Southampton2onermUnequalSampleSizes()
y,A,B,SUBJ = dataset.get_data()
print( dataset )



#(1) Run ANOVA:
FF        = spm1d.stats.anova2onerm(y, A, B, SUBJ)
FFi       = FF.inference(0.05)
print( FFi )


