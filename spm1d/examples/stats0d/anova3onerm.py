
import spm1d




#(0) Load dataset:
dataset      = spm1d.data.uv0d.anova3onerm.NYUCaffeine()
dataset      = spm1d.data.uv0d.anova3onerm.Southampton3onerm()
y,A,B,C,SUBJ = dataset.get_data()
print dataset



#(1) Run ANOVA:
F = spm1d.stats.anova3onerm(y, A, B, C, SUBJ, equal_var=True)
Fvalues = [f.z for f in F]
print Fvalues


