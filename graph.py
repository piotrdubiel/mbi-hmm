import matplotlib.pyplot as plt
import matplotlib.mlab as mlab

fig = plt.figure()
ax = fig.add_subplot(111)

ax.hist([1, 2,3,4], 50, normed=1)

plt.show()
