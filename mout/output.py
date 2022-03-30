import mcol
import sys                                    # sys.argv

import numpy as np

from .convert import toPrecision

def out(string,printScript=False,colour="",end="\n"):
  if printScript:
    thisScript = sys.argv[0]                                    # get name of script
    print(mcol.func+thisScript+mcol.clear+": ",end='')
  print(colour+string+mcol.clear,flush=True,end=end)

def headerOut(string,printScript=False,prefix=None,end="\n",dataFile=None,verbosity=1):
  if verbosity > 0:
    if printScript:
      thisScript = sys.argv[0]                                    # get name of script
      print(mcol.func+thisScript+mcol.clear+":",end=' ')
    if prefix is not None:
      print(mcol.bold+prefix,end=' ')
    string = str(string)
    print(mcol.bold+string+mcol.clear,flush=True,end=end)

  if dataFile is not None:
    dataFile.write("# ")
    if prefix is not None:
      dataFile.write(prefix)
    dataFile.write(string)
    dataFile.write('\n')

def debugOut(string):
  headerOut(string,prefix=mcol.debug+">>>")

def varOut(name, value, unit="",error=None,valCol="",precision=8,errorPrecision=2,printScript=False,end="\n",dataFile=None,verbosity=1,sf=True,list_length=True,integer=False):
  
  assert isinstance(name,str)
  assert np.array(value).ndim < 2

  nameStr = mcol.varName+name+mcol.clear

  if integer:
    sf=False
    precision=0

  if verbosity > 0:
    if printScript:
      thisScript = sys.argv[0]                                    # get name of script
      print(mcol.func+thisScript+mcol.clear+": ",end='')

    if type(value) is str:
      valueStr = value
    elif isinstance(value,bool):
      valueStr = str(value)
    elif isinstance(value,list):
      valueStr = toPrecision(value,precision,sf=sf)
      if list_length: nameStr += "[#="+str(len(value))+"]"
    elif isinstance(value,np.ndarray):
      if np.ndim(value) != 1:
        valueStr = str(value)
      else:
        valueStr = toPrecision(list(value),precision,sf=sf)
        if list_length: nameStr += "[#="+str(len(value))+"]"
    elif type(value) is int:
      valueStr = str(value)
    else:
      valueStr = toPrecision(value,precision,sf=sf)
    
    # print(type(nameStr))
    # print(type(valueStr))

    if error is None:
      print(nameStr
            +" = "+valCol+valueStr+mcol.clear
            +mcol.varType+" "+unit+mcol.clear,flush=True,end=end)
    else:
      errorStr = toPrecision(error,errorPrecision,sf=sf)
      print(nameStr
            +" = "+valCol+valueStr+mcol.clear
            +" +/- "+valCol+errorStr+mcol.clear
            +mcol.varType+" "+unit+mcol.clear,flush=True,end=end)

  if dataFile is not None:
    if error is None:
      dataFile.write(name+", "+str(value)+", "+unit)
    else:
      dataFile.write(name+", "+str(value)+", "+str(error)+", "+unit)
    dataFile.write('\n')

def warningOut(string,printScript=False,code=None,end="\n"):

  from .progress import _ACTIVE_PROGRESS_
  if _ACTIVE_PROGRESS_:
    print("\r",flush=True,end='')

  if printScript:
    thisScript = sys.argv[0]                                    # get name of script
    print(mcol.func+thisScript+mcol.clear+": ",end='')
  print(mcol.warning+"Warning: "+string,end='')
  if code is not None: 
    print(mcol.warning+" [code="+str(code)+"]",end='')
  print(mcol.clear,flush=True,end=end)

def errorOut(string,printScript=False,fatal=False,code=None,end="\n"):

  from .progress import _ACTIVE_PROGRESS_
  if _ACTIVE_PROGRESS_:
    print("\n",flush=True,end='')

  if printScript:
    thisScript = sys.argv[0]                                    # get name of script
    print(mcol.func+thisScript+mcol.clear+": ",end='')
  if fatal:
    prefix = "Fatal Error: "
  else:
    prefix = "Error: "
  print(mcol.error+prefix+string+mcol.error,end='')
  if code is not None: 
    print(mcol.error+" [code="+str(code)+"]",end='')
  print(mcol.clear,flush=True,end=end)
  if fatal: exit()

def successOut(string,printScript=False,prefix=None,end="\n"):
  if printScript:
    thisScript = sys.argv[0]                                    # get name of script
    print(mcol.func+thisScript+mcol.clear+":",end=' ')
  if prefix is not None:
    print(mcol.success+prefix,end=' ')
  print(mcol.success+string+mcol.clear,flush=True,end=end)

def differenceOut(name, value1, value2, unit="",valCol="",precision=8,diffPrecision=2,printScript=False,end="\n",dataFile=None,verbosity=1):
  if verbosity > 0:
    if printScript:
      thisScript = sys.argv[0]                                    # get name of script
      print(mcol.func+thisScript+mcol.clear+": ",end='')

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

  if dataFile is not None:
    dataFile.write(name+", "+diffStr+", "+pcntStr)
    dataFile.write('\n')

  return difference, pcnt_diff

def percentage_difference(value1,value2):
  return 200*(value2-value1)/(value1+value2)

  # if dataFile is not None:
  #   if error is None:
  #     dataFile.write(name+", "+str(value)+", "+unit)
  #   else:
  #     dataFile.write(name+", "+str(value)+", "+str(error)+", "+unit)
  #   dataFile.write('\n')
