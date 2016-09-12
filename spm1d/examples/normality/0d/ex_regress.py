
import spm1d



#(0) Load dataset:
dataset = spm1d.data.uv0d.regress.RSRegression()
dataset = spm1d.data.uv0d.regress.ColumbiaHeadCircumference()
y,x     = dataset.get_data()



#(1) Conduct normality test:
alpha      = 0.05
spmi       = spm1d.stats.normality.k2.regress(y, x).inference(alpha)
print( spmi )


