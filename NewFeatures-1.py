import spm1d
YA,YB = spm1d.data.uv1d.t2.SimulatedTwoLocalMax().get_data()
t = spm1d.stats.ttest2(YB, YA)
ti = t.inference(0.05)
ti.plot()
ti.plot_p_values()