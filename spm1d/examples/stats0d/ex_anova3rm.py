
import spm1d





#(0) Load dataset:
dataset      = spm1d.data.uv0d.anova3rm.SPM1D2x2x2()
# dataset      = spm1d.data.uv0d.anova3rm.SPM1D2x3x5()
# dataset      = spm1d.data.uv0d.anova3rm.SPM1D3x3x3()
y,A,B,C,SUBJ = dataset.get_data()
print( dataset )




#(1) Run ANOVA:
FF        = spm1d.stats.anova3rm(y, A, B, C, SUBJ, equal_var=True)
FFi       = FF.inference(0.05)
print( FFi )

