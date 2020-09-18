
# # _ACTIVE_PROGRESS_ = False
# ###

# import sys

# # this is a pointer to the module object instance itself.
# this = sys.modules[__name__]

# # we can explicitly make assignments on it 
# this._ACTIVE_PROGRESS_ = False

# ###

from .output import out
from .output import varOut
from .output import headerOut
from .output import debugOut
from .output import warningOut
from .output import errorOut
from .output import successOut
from .output import differenceOut

from .progress import progress

from .convert import toPrecision # documentation missing
from .convert import str2bool # documentation missing

from .fileio import append2file # documentation missing

from .print import blockPrint
from .print import enablePrint
from .print import redirectPrint
