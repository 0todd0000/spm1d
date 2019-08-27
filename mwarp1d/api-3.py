from matplotlib import pyplot as plt
import mwarp1d
# >>>
k = mwarp1d.gaussian_half_kernel(10, 3, 51, reverse=True)
# >>>
plt.figure()
plt.plot(k)
plt.show()
