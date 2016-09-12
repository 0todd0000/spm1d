
import spm1d



#(0) Load dataset:
dataset    = spm1d.data.uv0d.anova2rm.Antidepressant()
dataset    = spm1d.data.uv0d.anova2rm.RSXLTraining()
dataset    = spm1d.data.uv0d.anova2rm.SocialNetworks()
dataset    = spm1d.data.uv0d.anova2rm.Southampton2rm()
y,A,B,SUBJ = dataset.get_data()
print( dataset )




#(1) Conduct normality test:
alpha      = 0.05
spmi       = spm1d.stats.normality.k2.anova2rm(y, A, B, SUBJ).inference(alpha)
print( spmi )