
# setting colours
import matplotlib as mpl
from cycler import cycler
mpl.rcParams['axes.prop_cycle'] = cycler(color=['#e91c00','#007dbe','#00A87C',"#EAA900","#A000DE","#5FBDEF","#F2E82D","#FF0000","#0700FF","#00FF00","#FFAE00","#F18CF4","#00FFFF"])

from .main import show

from .graph2D import graph2D
from .graph2D import chart2D

# from .fit import constFit
# from .fit import linFit

from .fit import fit
from .fit import getCoeffStr