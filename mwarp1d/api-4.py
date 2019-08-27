from matplotlib import pyplot as plt
import mwarp1d
# >>>
k = mwarp1d.gaussian_half_kernel(10, 3, 51, reverse=True)
ki = mwarp1d.interp1d(k, 200)
# >>>
plt.figure()
plt.plot(k, label='Original')
plt.plot(ki, label='Interpolated')
plt.legend()
plt.show()
