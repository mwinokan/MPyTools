
import mcol # https://github.com/mwinokan/MPyTools
import mout # https://github.com/mwinokan/MPyTools

# matplotlib.use("tkagg")

import matplotlib as mpl
import os
if "scarf" in os.popen("hostname").read():
  if not "ui3" in os.popen("hostname").read():
    # print("Using agg for Matplotlib")
    mpl.use('agg')

import matplotlib.pyplot as plt

import numpy as np

"""

  To-Do's
    * Close after saving argument?

"""

def checkdata(dataset):

	# check if its a single set of three lists
	if len(dataset) == 3:
		# [?, ?, ?]
		if all([isinstance(thing,list) for thing in dataset]):
			# [[?], [?], [?]]
			if all([not isinstance(thing[0],list) for thing in dataset]):
				# [[not list],[not list],[not list]]
				return True

	# could be a list of valid data sets
	for data in dataset:
		if checkdata(data) is not True:
			return False

	return [True]

def surf3D(dataset,show=True,filename=None):

	'''

		dataset must be a list of [xdata,ydata,zdata]

	'''

	validity = checkdata(dataset)

	if validity is False:
		mout.errorOut("Incompatible data",fatal=True)

	many = False
	if validity == [True]:
		many = True

	from mpl_toolkits.mplot3d import axes3d

	fig = plt.figure(num=1, clear=True)
	ax = fig.add_subplot(1, 1, 1, projection='3d')

	if not many:
		# ax.plot_surface(np.array(dataset[0]),np.array(dataset[1]),np.array(dataset[2]))
		ax.plot_trisurf(np.array(dataset[0]),np.array(dataset[1]),np.array(dataset[2]))
		# ax.scatter(np.array(dataset[0]),np.array(dataset[1]),np.array(dataset[2]))

	fig.tight_layout()

	if show:
		plt.show()
		# fig.show()

	if filename is not None:
	    fig.savefig(filename)
