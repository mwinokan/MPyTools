
import mcol # https://github.com/mwinokan/MPyTools
import math
import sys

def progress(current,maximum,prepend=None,append="",width=20,fill="#",printScript=False):
  percentage = mcol.result + "{:>6.2f}%".format(current/maximum*100) + mcol.clear
  if prepend is not None: 
    prepend = mcol.varName + prepend + mcol.clear + " = "
  else:
    prepend = ""
  if printScript:
    thisScript = sys.argv[0]                                    # get name of script
    prepend = mcol.func+thisScript+mcol.clear+": "
  this_fill = math.floor((current/maximum)*width)
  if current != 0:
    prepend = "\r" + prepend
  if this_fill == width:
    append = append + "\n"
  filling = "".rjust(this_fill,fill)
  filling = filling.ljust(width, ' ')
  bar = "[" + filling + "] "
  print(prepend + bar + percentage + append,flush=True,end='')
