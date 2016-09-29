
import spm1d




#(0) Load dataset:
dataset    = spm1d.data.uv0d.anova2rm.Antidepressant()
# dataset    = spm1d.data.uv0d.anova2rm.RSXLTraining()
# dataset    = spm1d.data.uv0d.anova2rm.SocialNetworks()
# dataset    = spm1d.data.uv0d.anova2rm.Southampton2rm()
# dataset    = spm1d.data.uv0d.anova2rm.SPM1D3x3()
# dataset    = spm1d.data.uv0d.anova2rm.SPM1D3x4()
# dataset    = spm1d.data.uv0d.anova2rm.SPM1D3x5()
# dataset    = spm1d.data.uv0d.anova2rm.SPM1D4x4()
# dataset    = spm1d.data.uv0d.anova2rm.SPM1D4x5()
y,A,B,SUBJ = dataset.get_data()
print( dataset )





#(1) Run ANOVA:
FF        = spm1d.stats.anova2rm(y, A, B, SUBJ)
FFi       = FF.inference(0.05)
print( FFi )







