import matplotlib.pyplot as plt
import matplotlib.mlab as mlab


plt.plot(range(10), range(10))
plt.title("Simple Plot")
plt.show()

fig = plt.figure()
ax = fig.add_subplot(111)

ax.hist([(1,0.5),(2,0.1),(3,0.2),(4,1.1)], 50, normed=1)

plt.savefig('foo.png')
