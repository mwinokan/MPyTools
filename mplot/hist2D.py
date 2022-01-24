
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

def hist2D(xdata,ydata,
           bins=10,
           xlab='x',ylab='y',
           title=None,
           filename=None,
           show=True,
           verbosity=2,density=False,
           printScript=False,xmin=None,xmax=None,ymin=None,ymax=None,dpi=100,figsize=[4.8,6.4]):

  if (verbosity > 0):
    if title is not None:
      mout.out("graphing "+mcol.varName+
               title+
               mcol.clear+" ... ",
               printScript=printScript,
               end='')
    else:
      mout.out("graphing ... ",
               printScript=printScript,
               end='')

  many = any(isinstance(el,list) for el in ydata)

  assert not many

  if not any([thing is None for thing in [xmin,xmax,ymin,ymax]]):
    range = [[xmin,xmax],[ymin,ymax]]
  else:
    range = None

  graph, axis = plt.subplots(dpi=dpi,figsize=figsize)

  plt.hist2d(xdata,ydata,bins=bins,range=range,density=density)

  plt.xlabel(xlab)
  plt.ylabel(ylab)
  plt.suptitle(title)

  if show:
    plt.show()

  if filename is not None:
    if (verbosity > 0):
      mout.out("saving as " + mcol.file + filename + mcol.clear + " ... ",end='')
    plt.savefig(filename)

  plt.close()

  if (verbosity > 0):
    mout.out("Done.")

