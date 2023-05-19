import mcol
import sys                                    # sys.argv

import numpy as np
import os

from .convert import toPrecision

__SHOW_DEBUG__ = True

def out(string,colour="",end="\n"):
  print(f'{colour}{string}{mcol.clear}',flush=True,end=end)

def headerOut(string,prefix=None,end="\n"):
  str_buffer = ''
  if prefix:
    str_buffer += f'{mcol.bold}{prefix} '
  string = str(string)
  str_buffer += f'{mcol.bold}{string}{mcol.clear}'
  out(str_buffer,end=end)

def debugOut(string):
  global __SHOW_DEBUG__
  if __SHOW_DEBUG__: 
    headerOut(string,prefix=mcol.debug+">>>")

def hideDebug():
  global __SHOW_DEBUG__
  __SHOW_DEBUG__ = False

def showDebug():
  global __SHOW_DEBUG__
  __SHOW_DEBUG__ = True

def varOut(name, value, unit="",error=None,valCol="",precision=8,errorPrecision=2,end="\n",verbosity=1,sf=True,list_length=True,integer=False):
  
  ## to-do: value precision based on error sig figs

  str_buffer = ''
  nameStr = f'{mcol.varName}{name}{mcol.clear}'

  if integer:
    sf=False
    precision=0

  if type(value) is set:
    value = list(value)

  if type(value) is str:
    valueStr = value
  elif isinstance(value,bool):
    valueStr = str(value)
  elif isinstance(value,list):
    valueStr = toPrecision(value,precision,sf=sf)
    if list_length: 
      nameStr += f"[#={len(value)}]"
  elif isinstance(value,np.ndarray):
    if np.ndim(value) != 1:
      valueStr = str(value)
    else:
      valueStr = toPrecision(list(value),precision,sf=sf)
      if list_length: 
        nameStr += f"[#={len(value)}]"
  elif type(value) is int:
    valueStr = str(value)
  else:
    valueStr = toPrecision(value,precision,sf=sf)
  
  if error is None:
    str_buffer += f' = {valCol}{valueStr}{mcol.clear}{mcol.varType} {unit}{mcol.clear}'
    out(str_buffer,end=end)

  else:

    if isinstance(error,list):
      error = np.linalg.norm(error)      
    errorStr = toPrecision(error,errorPrecision,sf=sf)
    
    str_buffer += f' = {valCol}{valueStr}{mcol.clear} +/- {valCol}{errorStr}{mcol.varType} {unit}{mcol.clear}'
    out(str_buffer,end=end)
    
  if error is None:
    return value
  else:
    return value,error

def warningOut(string,code=None,end="\n"):
  from .progress import _ACTIVE_PROGRESS_
  if _ACTIVE_PROGRESS_:
    print("\r",flush=True,end='')
  print(mcol.warning+"Warning: "+string,end='')
  if code is not None: 
    print(mcol.warning+" [code="+str(code)+"]",end='')
  print(mcol.clear,flush=True,end=end)

def errorOut(string,fatal=False,code=None,end="\n"):

  from .progress import _ACTIVE_PROGRESS_
  if _ACTIVE_PROGRESS_:
    print("\n",flush=True,end='')

  if fatal:
    prefix = "Fatal Error: "
  else:
    prefix = "Error: "
  try:
    print(mcol.error+prefix+string+mcol.error,end='')
  except TypeError:
    print(mcol.error+prefix+str(string)+mcol.error,end='')
  if code is not None: 
    print(mcol.error+" [code="+str(code)+"]",end='')
  print(mcol.clear,flush=True,end=end)
  if fatal: exit()

def successOut(string,prefix=None,end="\n"):
  if prefix is not None:
    print(mcol.success+prefix,end=' ')
  print(mcol.success+string+mcol.clear,flush=True,end=end)

def differenceOut(name, value1, value2, unit="",valCol="",precision=8,diffPrecision=2,end="\n",verbosity=1):

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
