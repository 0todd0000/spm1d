
import matplotlib.pyplot as plt
import spm1d



#(0) Load data:
dataset      = spm1d.data.mv1d.manova1.Dorn2012()
Y,A          = dataset.get_data()  #A:slow, B:fast
print( dataset )



#(1) Conduct test:
alpha        = 0.05
X2           = spm1d.stats.manova1(Y, A)
X2i          = X2.inference(0.05)



#(2) Plot:
plt.close('all')
X2i.plot()
X2i.plot_p_values()
plt.tight_layout()
plt.show()


