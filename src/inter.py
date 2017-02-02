import numpy as np
from numpy import nan
from scipy import interpolate as ip
import matplotlib.pyplot as plt


x = np.linspace(0, 20, 201)
np.random.shuffle(x)

x0 = sorted(x[:150])
x = sorted(x)
y0 = np.sin(x0)

tpl = ip.splrep(x0, y0, k=3)
y = ip.splev(x, tpl)

plt.figure()
plt.plot(x0, y0, 'o-')
plt.plot(x, y, 'x-')
plt.title("Interpolated function.")
plt.show()



