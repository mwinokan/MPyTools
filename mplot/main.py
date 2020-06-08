
import mcol # https://github.com/mwinokan/MPyTools
import mout # https://github.com/mwinokan/MPyTools

import matplotlib
matplotlib.use("tkagg")
import matplotlib.pyplot as plt

def showAll(verbosity=1):
  if (verbosity > 0):
    mout.out("showing all graphs"+" ... ",
             printScript=True,
             end='')

  plt.show()

  if (verbosity > 0):
    mout.out("Done.")

def closeAll(verbosity=1):
  if (verbosity > 0):
    mout.out("closing all graphs"+" ... ",
             printScript=True,
             end='')

  plt.close(fig='all')

  if (verbosity > 0):
    mout.out("Done.")
