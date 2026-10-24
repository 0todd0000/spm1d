
import numpy as np
from matplotlib import pyplot
import spm1d



# load dataset:
Y,A,B     = spm1d.util.get_dataset('Dorn2012')


# run ANOVA:
FF      = spm1d.stats.anova2(Y, A, B, model='full', equal_var=True)
FFi     = [F.inference(0.05)  for F in FF]


# plot:
pyplot.close('all')
# constants:
labels  = ['Main effect: FOOT', 'Main effect: SPEED', 'Interaction effect']
# create axes:
pyplot.figure(figsize=(13,4))
xx  = np.linspace(0.05, 0.7, 3)
ax0 = pyplot.axes([xx[0],0.14,0.27,0.8])
ax1 = pyplot.axes([xx[1],0.14,0.27,0.8])
ax2 = pyplot.axes([xx[2],0.14,0.27,0.8])
AX  = ax0,ax1,ax2
### plot inference objects:
FFi[0].plot(ax=ax0)
FFi[1].plot(ax=ax1)
FFi[2].plot(ax=ax2)
### annotate:
[ax.set_ylim(0, 115)  for ax in AX]
[ax.set_xlabel('Time (%)', size=16)  for ax in AX]
tx  = [ax.text(0.4, 0.85, '%s'%label, transform=ax.transAxes)  for ax,label in zip(AX,labels)]
pyplot.setp(tx, size=16)
# pyplot.show()