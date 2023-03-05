import matplotlib.pyplot as plt
import power1d

data = power1d.data.weather()   #load data dictionary
y    = data['Continental']   #extract one region
plt.plot(y.T, color="k")