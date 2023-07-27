
import mcol # https://github.com/mwinokan/MPyTools
import math
import sys

try:
  import emoji
  EMOJI_SUPPORTED = True
except ModuleNotFoundError:
  EMOJI_SUPPORTED = False

ACTIVE_PROGRESS = 0

def progress(current,maximum,reverse=False,prepend="",append=None,width=20,fill="#"):

  global ACTIVE_PROGRESS

  if EMOJI_SUPPORTED and len(list(emoji.analyze(fill))):
    width = width // 2
    fill_is_emoji = True
  else:
    fill_is_emoji = False

  if reverse:
    current = maximum - current

  # if done
  if current/maximum >= 1.00:
    current = maximum

  if append is not None:
    append = f' {append}'
  else:
    append = ''

  if prepend:
    ACTIVE_PROGRESS = len(prepend) + len(append) + width + 9
    prepend = mcol.varName + prepend + mcol.clear + " = "
  else:
    ACTIVE_PROGRESS = len(append) + width + 12
  
  # percentage string
  percentage = f"{mcol.result}{current/maximum*100:>6.2f}%{mcol.clear}"
  
  # number of fill characters
  this_fill = math.floor((current/maximum)*width)
  
  # if there is an active progress go back to start
  if ACTIVE_PROGRESS:
    prepend = "\r" + prepend

  # if completed add a newline
  if this_fill == width:
    ACTIVE_PROGRESS = 0
    append += "\n"

  # create the fill string
  if fill_is_emoji:
    filling = this_fill * fill
    filling = f'{filling}{"  "*(width - this_fill)}'
  else:
    filling = "".rjust(this_fill,fill)
    filling = filling.ljust(width, ' ')

  # create the bar string
  bar = "[" + filling + "] "
  
  # print the progress bar
  print(prepend + bar + percentage + append,flush=True,end='')
