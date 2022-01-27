
# setting colours
import matplotlib as mpl

import os
if "scarf" in os.popen("hostname").read():
  if not "ui3" in os.popen("hostname").read():
    print("Using agg for Matplotlib")
    mpl.use('agg')

from cycler import cycler
mpl.rcParams['axes.prop_cycle'] = cycler(color=['#e91c00','#007dbe','#00A87C',"#EAA900","#A000DE","#5FBDEF","#F2E82D","#FF0000","#0700FF","#00FF00","#FFAE00","#F18CF4","#00FFFF"])

from .main import showAll
from .main import closeAll

from .graph2D import graph2D
from .graph2D import chart2D
from .hist2D import hist2D
from .hist1D import hist1D
from .surf3D import surf3D

from .fit import fit
from .fit import getCoeffStr
