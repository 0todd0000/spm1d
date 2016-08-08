
import numpy as np
# import spm1dNP
import spm1d




#(0) Load dataset:
# dataset    = spm1d.data.uv1d.t1.Random()
# dataset    = spm1d.data.uv1d.t1.SimulatedPataky2015a()
dataset    = spm1d.data.uv1d.t1.SimulatedPataky2015b()
y,mu       = dataset.get_data()
# y  *= -1

# ### prepare stat computer:
# calculators = spm1dNP.calculators
# calc           = calculators.CalculatorTtest(y.shape[0], mu)
# z              = calc.get_test_stat(y)
#
#
#
#

# alpha      = 0.05
# two_tailed = True
#
# ### prepare permuter:
# permuters = spm1dNP.permuters
# perm      = permuters.PermuterTtest1D(y, mu)
# z0        = perm.get_test_stat_original()
# perm.build_pdf()
#
# alpha0    = 0.5*alpha if two_tailed else alpha
# zstar     = perm.get_z_critical(alpha=alpha0, two_tailed=two_tailed)
# if two_tailed:
# 	zstar = zstar[1]
#
# print zstar
# perm.set_metric( 'MaxClusterIntegral' )
# perm.build_secondary_pdf(zstar)
# clusters  = perm.get_clusters(z0, zstar, two_tailed=two_tailed)
#
#
# print clusters
#
# # p         = perm.get_cluster_p_values(z0, zstar)




# from matplotlib import pyplot
# pyplot.close('all')
# pyplot.figure(figsize=(8,6))
# pyplot.get_current_fig_manager().window.move(0, 0)
# ax = pyplot.axes()
# ax.plot( z )
# ax.plot( z0 )
# pyplot.show()



#(1) Conduct non-parametric test:
alpha      = 0.05
two_tailed = False
t          = spm1d.stats.nonparam.ttest(y, mu)
# # ti         = t.inference(alpha, two_tailed=two_tailed, iterations=-1)
# # # print ti
# # print ti.clusters
# #
# #
# # #(2) Compare with parametric result:
# # tparam     = spm1d.stats.ttest(y, mu)
# # tiparam    = tparam.inference(alpha, two_tailed=two_tailed)
# #
# #
# #
# # from matplotlib import pyplot
# # pyplot.close('all')
# # pyplot.figure(figsize=(12,4))
# # pyplot.get_current_fig_manager().window.move(0, 0)
# # ax = pyplot.subplot(121);  tiparam.plot(ax=ax)
# # ax = pyplot.subplot(122);  ti.plot(ax=ax)
# # pyplot.show()
# #






# print(ti)
#
#
# #(2) Compare to parametric inference:
# results    = scipy.stats.ttest_1samp(y, mu)
# tparam     = results.statistic
# pparam     = get_scipy_pvalue(results, two_tailed )
#
#
# #(3) Compare to parametric test:
# print
# print( 'Non-parametric results:' )
# print( '   t=%.3f, p=%.5f' %(ti.z, ti.p) )
# print
# print( 'Parametric results:' )
# print( '   t=%.3f, p=%.5f' %(tparam, pparam) )
# print
#

