
import mcol # https://github.com/mwinokan/MPyTools
import mout # https://github.com/mwinokan/MPyTools

import matplotlib
matplotlib.use("tkagg")
import matplotlib.pyplot as plt

def show(verbosity=1):
  if (verbosity > 0):
    mout.out("showing graphs"+" ... ",
             printScript=True,
             end='')

  plt.show()

  if (verbosity > 0):
    mout.out("Done.")