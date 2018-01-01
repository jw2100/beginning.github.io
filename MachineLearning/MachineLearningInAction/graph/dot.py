

from matplotlib
from matplotlib.pyplot as plt
from numpy import array

#散点
fig = plt.figure()
ax = fig.add_subplot(111)
ax.scatter(datingDataMat[:,1], datingDataMat[:2])
ax.scatter(datingDataMat[:,1], datingDataMat[:2], 15.0*array(datingLabels), 15.0*array(datingLabels))
plt.show()



#数