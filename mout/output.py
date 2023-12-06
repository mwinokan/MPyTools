import mcol
import sys                                    # sys.argv

import numpy as np
import os

from .convert import toPrecision

from collections.abc import KeysView

SHOW_DEBUG = True
PARTIAL_LINE = False

def clear_line(term_width=None):
  try:
    term_width = term_width or os.get_terminal_size()[0]
  except OSError:
    term_width = 60

  empty = "".join([" "]*term_width)
  print(f'\r{empty}\r',end='')

def out(string,colour="",this_len=None,end="\n",is_progress=False):

  global PARTIAL_LINE
  from .progress import ACTIVE_PROGRESS, ACTIVE_PROGRESS_TEXT

  string = str(string)

  if not PARTIAL_LINE:
    clear_line()

  if end != '\n':
    PARTIAL_LINE = True
  else:
    PARTIAL_LINE = False

  print(f'{colour}{string}{mcol.clear}',flush=True,end=end)

  if not is_progress and ACTIVE_PROGRESS:
    clear_line()
    if PARTIAL_LINE:
      print('')
    print(ACTIVE_PROGRESS_TEXT,flush=True,end='')

def underline(string, end='\n'):
  out(f'{mcol.underline}{string}',end=end)

def header(string,prefix=None,end='\n'):
  headerOut(string,prefix,end)

def headerOut(string,prefix=None,end="\n"):

  from .progress import ACTIVE_PROGRESS, ACTIVE_PROGRESS_TEXT
  if ACTIVE_PROGRESS:
    clear_line()
  elif PARTIAL_LINE:
    print('')

  str_buffer = ''
  this_len = 0
  if prefix:
    str_buffer += f'{mcol.bold}{prefix} '
    this_len += len(prefix) + 1

  string = str(string)
  str_buffer += f'{mcol.bold}{string}{mcol.clear}'
  this_len += len(string)
  out(str_buffer,this_len=this_len,end=end)

def debug(string):
  debugOut(string)

def debugOut(string):
  global SHOW_DEBUG
  if SHOW_DEBUG: 
    headerOut(string,prefix=mcol.debug+">>>")

def hideDebug():
  global SHOW_DEBUG
  SHOW_DEBUG = False

def showDebug():
  global SHOW_DEBUG
  SHOW_DEBUG = True

def var(name, value, unit="",error=None,valCol="",precision=8,errorPrecision=2,end="\n",verbosity=1,sf=True,list_length=True,integer=False,symbol='='):
  varOut(name,value,unit,error,valCol,precision,errorPrecision,end,sf,list_length,integer,symbol)

def varOut(name, value, unit="",error=None,valCol="",precision=8,errorPrecision=2,end="\n",sf=True,list_length=True,integer=False,symbol='='):
  
  ## to-do: value precision based on error sig figs

  from .progress import ACTIVE_PROGRESS, ACTIVE_PROGRESS_TEXT
  if ACTIVE_PROGRESS:
    clear_line()
  elif PARTIAL_LINE:
    print('')

  nameStr = f'{mcol.varName}{name}{mcol.clear}'

  if integer:
    sf=False
    precision=0

  if value is None:
    value = "None"

  if isinstance(value,set):
    value = list(value)

  if isinstance(value,KeysView):
    value = list(value)

  if type(value) is str:
    valueStr = value
    this_len = len(valueStr)
  elif isinstance(value,bool):
    valueStr = str(value)
    this_len = len(valueStr)
  elif isinstance(value,list):
    valueStr = toPrecision(value,precision,sf=sf)
    this_len = len(valueStr)
    if list_length: 
      nameStr += f"[#={len(value)}]"
      this_len += len(f"[#={len(value)}]")
  elif isinstance(value,np.ndarray):
    if np.ndim(value) != 1:
      valueStr = str(value)
      this_len = len(valueStr)
    else:
      valueStr = toPrecision(list(value),precision,sf=sf)
      this_len = len(valueStr)
      if list_length: 
        nameStr += f"[#={len(value)}]"
        this_len += len(f"[#={len(value)}]")
  elif type(value) is int:
    valueStr = str(value)
    this_len = len(valueStr)
  else:
    valueStr = toPrecision(value,precision,sf=sf)
    this_len = len(valueStr)
  
  str_buffer = nameStr

  if error is None:
    str_buffer += f' {symbol} {valCol}{valueStr}{mcol.clear}{mcol.varType} {unit}{mcol.clear}'
    this_len += 4 + len(valueStr) + len(unit)

  else:

    if isinstance(error,list):
      error = np.linalg.norm(error)      
    errorStr = toPrecision(error,errorPrecision,sf=sf)
    
    this_len += 9 + len(errorStr) + len(valueStr) + len(unit)
    str_buffer += f' {symbol} {valCol}{valueStr}{mcol.clear} +/- {valCol}{errorStr}{mcol.varType} {unit}{mcol.clear}'
  
  out(str_buffer,this_len=this_len,end=end)
    
  if error is None:
    return value
  else:
    return value,error

def warning(string,code=None,end="\n"):
  warningOut(string,code,end)

def warningOut(string,code=None,end="\n"):
  
  from .progress import ACTIVE_PROGRESS, ACTIVE_PROGRESS_TEXT
  if ACTIVE_PROGRESS:
    clear_line()
  elif PARTIAL_LINE:
    print('')

  str_buffer = f'{mcol.warning}Warning: {string}'
  this_len = 9 + len(string)
  if code is not None: 
    this_len += 8 + len(code)
    str_buffer += f" {mcol.warning}[code={code}]"
  str_buffer += mcol.clear
  out(str_buffer,this_len=this_len,end=end)

def error(string,fatal=False,code=None,end="\n"):
  errorOut(string,fatal,code,end)

def errorOut(string,fatal=False,code=None,end="\n"):
  
  from .progress import ACTIVE_PROGRESS, ACTIVE_PROGRESS_TEXT
  if ACTIVE_PROGRESS:
    clear_line()
  elif PARTIAL_LINE:
    print('')

  if fatal:
    str_buffer = f"{mcol.error}Fatal Error: "
    this_len = 13
  else:
    str_buffer = f"{mcol.error}Error: "
    this_len = 7

  string = str(string)

  str_buffer += string
  this_len += len(string)
  
  if code is not None: 
    this_len += 8 + len(code)
    str_buffer += f'{mcol.error} [code={code}]'
    
  str_buffer += mcol.clear
  out(str_buffer,this_len=this_len,end=end)

  if fatal: 
    exit()

def success(string,end="\n"):
  successOut(string,end)

def successOut(string,end="\n"):
  
  from .progress import ACTIVE_PROGRESS, ACTIVE_PROGRESS_TEXT
  if ACTIVE_PROGRESS:
    clear_line()
  elif PARTIAL_LINE:
    print('')

  out(f'{mcol.success}{string}{mcol.clear}',this_len=len(string),end=end)

def differenceOut(name, value1, value2, unit="",valCol="",precision=8,diffPrecision=2,end="\n",verbosity=1):

  from .progress import ACTIVE_PROGRESS, ACTIVE_PROGRESS_TEXT
  if ACTIVE_PROGRESS:
    clear_line()
  elif PARTIAL_LINE:
    print('')

  if type(value1) is int:
    valueStr1 = str(value1)
  else:
    valueStr1 = toPrecision(value1,precision)
  
  if type(value2) is int:
    valueStr2 = str(value2)
  else:
    valueStr2 = toPrecision(value2,precision)

  difference = value2-value1
  pcnt_diff = percentage_difference(value1,value2)

  diffStr = toPrecision(difference,precision)

  pcntStr = toPrecision(pcnt_diff,diffPrecision,sf=False)
  
  print(mcol.varName+name+mcol.clear
        +": Δ("+valCol+valueStr1+mcol.clear
        +", "+valCol+valueStr2+mcol.clear
        +") = "+valCol+diffStr+mcol.clear
        +mcol.varType+" "+unit+mcol.clear
        +" = "+valCol+pcntStr+mcol.clear
        +mcol.varType+" % "+mcol.clear,flush=True,end=end)

  return difference, pcnt_diff

def percentage_difference(value1,value2):
  return 200*(value2-value1)/(value1+value2)

def json(data):
  import json as js
  strbuff = js.dumps(data,indent=2)
  print(strbuff)
