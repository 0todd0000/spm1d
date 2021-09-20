
import numpy as np
import matplotlib.pyplot as plt
import spm1d



#(0) Load data:
np.random.seed(1)
y0         = spm1d.data.uv1d.normality.NormalityAppendixDataset('A1').Y
y1         = spm1d.data.uv1d.normality.NormalityAppendixDataset('A2').Y
y2         = spm1d.data.uv1d.normality.NormalityAppendixDataset('A3').Y


#(1) Compute normality metrics:
K2         = [spm1d.stats.normality.dagostinoK2(yy).inference(0.05)  for yy in [y0,y1,y2]]
P          = [spm1d.stats.normality.shapirowilk(yy)[1]  for yy in [y0,y1,y2]]
logP       = -np.log10(P)



#(2) Plot:
plt.close('all')
figw       = 8
figh       = figw / 1.6
plt.figure(figsize=(figw,figh))
### create axes:
axw = axh  = 0.27
axx,axy    = np.linspace(0.07, 0.71, 3), np.linspace(0.72, 0.09, 3)
AX         = np.array(  [[plt.axes([xx, yy, axw, axh])  for xx in axx]  for yy in axy]  )
### plot datasets:
[ax.plot(yy.T, 'k', lw=0.5)   for ax,yy in zip(AX[0], [y0,y1,y2])]
### plot K2 stats:
[k2i.plot(ax=ax, color='b')   for ax,k2i in zip(AX[1], K2)]
### plot Shapiro-Wilk p values:
[ax.plot(p, 'g', lw=2)   for ax,p in zip(AX[2], logP)]
### adjust axis tick labels:
[plt.setp(ax.get_xticklabels() + ax.get_yticklabels(), size=8 )   for ax in AX.flatten()]
plt.setp(AX[0], ylim=(-3.9,3.9))
plt.setp(AX[1], ylim=(0, 20))
plt.setp(AX[2], ylim=(0, 2.8))
plt.setp(AX[:2],   xticklabels=[])
plt.setp(AX[:,1:], yticklabels=[], ylabel='')
### axis labels:
[ax.set_xlabel('Time  (%)', size=14)   for ax in AX[2]]
ylabels   = '', r'$K^2$', r'$-\log_{10}(p)$'
[ax.set_ylabel(label, size=14)   for ax,label in zip(AX[:,0], ylabels)]
### dataset labels
[ax.text(0.5, 0.85, 'Dataset A%d'%(i+1), size=10, ha='center', bbox=dict(color='0.85'), transform=ax.transAxes)  for  i,ax in enumerate(AX[0])]
plt.show()







