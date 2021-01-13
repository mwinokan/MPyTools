
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

def hist1D(ydata,
           bins=10,
           xlab='x',ylab='y',
           title=None,
           filename=None,
           show=True,
           verbosity=2,density=False,
           printScript=False,
           range=None):

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

  plt.hist(ydata,bins=bins,range=range,density=density)

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

