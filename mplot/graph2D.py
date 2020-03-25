
import mcol # https://github.com/mwinokan/MPyTools
import mout # https://github.com/mwinokan/MPyTools

# import matplotlib
# matplotlib.use("tkagg")
import matplotlib.pyplot as plt

import numpy as np

"""

  To-Do's
    * Average (constfit), Running Averages
    * Close after saving argument?

"""

def graph2D(xdata,ydata,ytitles=None,filename=None,show=True,xmin=None,xmax=None,ymin=None,ymax=None,xlab='x',ylab='y',title=None,verbosity=2):

  plt.figure()

  if (verbosity > 1):
    if title is not None:
      mout.out("graphing "+mcol.varName+
               title+
               mcol.clear+" ... ",
               printScript=True,
               end='')
    else:
      mout.out("graphing ... ",
               printScript=True,
               end='')

  many = any(isinstance(el,list) for el in ydata)

  if many:
    # ydata is a list of lists!
    if ytitles is not None:
      for curve, label in zip(ydata,ytitles):
        plt.plot(xdata,curve,label=label)
    else:
      for i,curve in enumerate(ydata):
        plt.plot(xdata,curve,label="ydata["+str(i)+"]")
  else: 
    # ydata is just a list!
    plt.plot(xdata,ydata)

  plt.axis([xmin,xmax,ymin,ymax])
  plt.xlabel(xlab)
  plt.ylabel(ylab)
  plt.suptitle(title)

  if many:
    plt.legend()

  if show:
    if (verbosity > 0):
      mout.out("showing ... ",end='')
    plt.show()

  if filename is not None:
    if (verbosity > 0):
      mout.out("saving as " + mcol.file + filename + mcol.clear + " ... ",end='')
    plt.savefig(filename)

  if (verbosity > 1):
    mout.out("Done.")
