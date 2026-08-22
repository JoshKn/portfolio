import numpy as np
import matplotlib.pyplot as plt

f = 1   # frequency

x = np.arange(0, 2, 0.01) # rendering x-axis from 0 to 2 in steps of 0.01
y_1 = np.sin(2*np.pi * f * x) # sinus
y_2 = np.sin(np.pi/2 + 2*np.pi * f * x) # sinus + phase shift 1/4

plt.plot(x,y_1, x,y_2) # plotting both y values over x

plt.title("Sinus")
plt.xlabel("x")
plt.ylabel("y")

plt.show()
