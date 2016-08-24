
import spm1d




#(0) Load dataset:
dataset  = spm1d.data.uv0d.anova1rm.Abdi2010()
dataset  = spm1d.data.uv0d.anova1rm.Groceries()
# dataset  = spm1d.data.uv0d.anova1rm.Imacelebrity()
# dataset  = spm1d.data.uv0d.anova1rm.Southampton1rm()
y,A,SUBJ = dataset.get_data()
print( dataset )



#(1) Run ANOVA:
F = spm1d.stats.anova1rm(y, A, SUBJ, equal_var=True)
Fi = F.inference(0.05)
print( Fi )






