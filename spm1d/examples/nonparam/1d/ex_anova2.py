
import numpy as np
from matplotlib import pyplot
import spm1d




#(0) Load dataset:
dataset      = spm1d.data.uv1d.anova2.SPM1D_ANOVA2_2x2()
# dataset      = spm1d.data.uv1d.anova2.SPM1D_ANOVA2_2x3()
# dataset      = spm1d.data.uv1d.anova2.SPM1D_ANOVA2_3x3()
# dataset      = spm1d.data.uv1d.anova2.SPM1D_ANOVA2_3x4()
# dataset      = spm1d.data.uv1d.anova2.SPM1D_ANOVA2_3x5()
# dataset      = spm1d.data.uv1d.anova2.SPM1D_ANOVA2_4x4()
# dataset      = spm1d.data.uv1d.anova2.SPM1D_ANOVA2_4x5()
y,A,B        = dataset.get_data()



# roi = None
# permuters = spm1d.stats.nonparam.permuters
#
# perm = permuters.PermuterANOVA21D(y, roi, A, B)
# perm.build_pdf(100)
# zstarlist = perm.get_z_critical_list(0.05)
# print zstarlist
#
#
# self = perm
# i = 0
# zstar = zstarlist[i]
# a  = self.metric.get_max_metric(self.ZZ[:,i,:], zstar, circular)




# #(1) Conduct non-parametric test:
np.random.seed(0)
alpha      = 0.05
snpm       = spm1d.stats.nonparam.anova2(y, A, B)
print( snpm )



# print( snpm[0] )
# snpmi      = snpm.inference(alpha, iterations=200)
# # # # print snpmi
# # # # print snpmi.clusters
#
#
#
# #(2) Compare with parametric result:
# spm        = spm1d.stats.anova2(y, A, B, equal_var=True)
# spmi       = spm.inference(alpha)
# print spmi
# print spmi.clusters
#
#
#
# #(3) Plot
# pyplot.close('all')
# pyplot.figure(figsize=(12,4))
# pyplot.get_current_fig_manager().window.move(0, 0)
# ax0 = pyplot.subplot(121)
# ax1 = pyplot.subplot(122)
# labels = 'Parametric', 'Non-parametric'
# for ax,zi,label in zip([ax0,ax1], [spmi,snpmi], labels):
# 	zi.plot(ax=ax)
# 	zi.plot_threshold_label(ax=ax, fontsize=8)
# 	zi.plot_p_values(ax=ax, size=10)
# 	ax.set_title( label )
# pyplot.show()

