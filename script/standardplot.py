#---------------------------------------------------------------------------------------------#
# now let's have a llok at something a little more insteresting
# using matploting and NumPy
# install matplotlib from termil by typing: pip3 install matplotlib

import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

x = np.linspace(0, 20, 100)
plt.plot(x, np.sin(x))
plt.show()
#---------------------------------------------------------------------------------------------#
