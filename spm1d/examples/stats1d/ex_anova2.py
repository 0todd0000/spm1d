
import spm1d



'''
NOTE:  unbalanced designs are not yet supported.
   These datasets will generate errors because they are unbalanced.
'''

#(0) Load data:
dataset      = spm1d.data.uv1d.anova2.Besier2009kneeflexion()
# dataset      = spm1d.data.uv1d.anova2.Dorn2012()
Y,A,B        = dataset.get_data()




#(1) Conduct ANOVA:
alpha        = 0.05
F            = spm1d.stats.anova2(Y, A, B, equal_var=True)




