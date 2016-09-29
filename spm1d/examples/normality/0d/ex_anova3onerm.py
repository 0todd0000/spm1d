
import spm1d



#(0) Load dataset:
dataset      = spm1d.data.uv0d.anova3onerm.NYUCaffeine()
dataset      = spm1d.data.uv0d.anova3onerm.Southampton3onerm()
y,A,B,C,SUBJ = dataset.get_data()
print( dataset )




#(1) Conduct normality test:
alpha      = 0.05
spmi       = spm1d.stats.normality.k2.anova3onerm(y, A, B, C, SUBJ).inference(alpha)
print( spmi )



