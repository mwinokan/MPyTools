
import mcol # https://github.com/mwinokan/MPyTools
import math
# import sys
import os

from .output import clear_line, out

try:
  import emoji
  EMOJI_SUPPORTED = True
except ModuleNotFoundError:
  EMOJI_SUPPORTED = False

ACTIVE_PROGRESS = False
ACTIVE_PROGRESS_TEXT = False
PROGRESS_FILL = None
PROGRESS_VALUE = None
PROGRESS_MAXIMUM = None
PROGRESS_PREPEND = None
PROGRESS_APPEND = None

def progress(value,max_value,prepend=None,append=None,append_color=None,fill="#",width=None):

  global ACTIVE_PROGRESS, PROGRESS_FILL, PROGRESS_PREPEND, PROGRESS_VALUE, PROGRESS_MAXIMUM, PROGRESS_APPEND, ACTIVE_PROGRESS_TEXT

  # get the terminal width
  try:
    term_width = os.get_terminal_size()[0]
  except OSError:
    term_width = 60

  # clear the current line
  clear_line(term_width)

  # store progress parameters
  PROGRESS_APPEND = append
  PROGRESS_PREPEND = prepend
  PROGRESS_FILL = fill
  PROGRESS_VALUE = value
  PROGRESS_MAXIMUM = max_value

  # process prepend and append
  if prepend is not None:
    plen = len(prepend)+1
    prepend = f'{mcol.func}{prepend}{mcol.clear} '
  else:
    plen = 0
    prepend = ''

  if append is not None:
    alen = len(append)+1
    append = f' {append}'
  else:
    alen = 0
    append = ''

  if append_color is None:
    append_color = ''

  # calculate dynamic bar width
  bar_width = term_width - 11 - plen - alen

  # adjust for emoji
  if EMOJI_SUPPORTED and len(list(emoji.analyze(fill))):
    fill_is_emoji = True
    bar_width = bar_width//2
  else:
    fill_is_emoji = False

  # finish the progress bar
  if value == max_value:

    ACTIVE_PROGRESS = False
    
    fraction = 1.0
    prepend = prepend.rstrip(' ')
    # bar_filling = "".join([fill]*bar_width)
    # if bar_width > 0:
    #   bar = f'[{bar_filling}]'
    #   gap = ' '
    # else:
    #   bar = ''
    #   gap = ''
    end = '\n'

  # in progress bar    
  if value != max_value:

    ACTIVE_PROGRESS = True

    fraction = value/max_value

    if fill_is_emoji:
      bar_filling = "".join([fill]*(math.floor(bar_width*fraction)))
      bar_empty = "".join(["  "]*(bar_width-len(bar_filling)))

    else:
      bar_filling = "".join([fill]*math.floor(bar_width*fraction))
      bar_empty = "".join([" "]*(bar_width-len(bar_filling)))
    if bar_width > 0:
      bar = f'[{bar_filling}{bar_empty}]'
      gap = ' '
    else:
      bar = ''
      gap = ''
    end = ''

  # write
  if ACTIVE_PROGRESS:
    if bar_width < 0:
      append = f'{append[:bar_width]}+++'
      ACTIVE_PROGRESS_TEXT = f'{prepend}{mcol.clear}{bar}{gap}{mcol.result}{fraction:7.2%}{mcol.clear}{append_color}{append}'
      out(ACTIVE_PROGRESS_TEXT,end=end,is_progress=True)
    else:
      ACTIVE_PROGRESS_TEXT = f'{prepend}{mcol.clear}{bar}{gap}{mcol.result}{fraction:7.2%}{mcol.clear}{append_color}{append}'
      out(ACTIVE_PROGRESS_TEXT,end=end,is_progress=True)
  else:
    ACTIVE_PROGRESS_TEXT = False
    # if bar_width < 0:
    #   append = f'{append[:bar_width]}+++'
    out(f'{prepend}{mcol.clear}{append_color}{append}',end=end,is_progress=True)
    # out(f'{prepend}{mcol.clear}{bar}{gap}{mcol.result}{fraction:7.2%}{mcol.clear}{append_color}{append}',end=end,is_progress=True)

def finish():
  if ACTIVE_PROGRESS:
    progress(1,1,prepend=PROGRESS_PREPEND,append='OK',append_color=mcol.success,fill=PROGRESS_FILL)

def interrupt(append=None):
  global ACTIVE_PROGRESS

  import mcol
  
  if ACTIVE_PROGRESS:
    progress(PROGRESS_VALUE,PROGRESS_MAXIMUM,prepend=PROGRESS_PREPEND,append=f'{PROGRESS_APPEND} INTERRUPTED',append_color=mcol.error,fill=PROGRESS_FILL)
    print()
    ACTIVE_PROGRESS = False
    ACTIVE_PROGRESS_TEXT = False

