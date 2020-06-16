import mcol
import sys                                    # sys.argv

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
    print(mcol.bold+string+mcol.clear,flush=True,end=end)

  if dataFile is not None:
    dataFile.write("# ")
    if prefix is not None:
      dataFile.write(prefix)
    dataFile.write(string)
    dataFile.write('\n')

def varOut(name, value, unit="",error=None,valCol="",precision=8,errorPrecision=2,printScript=False,end="\n",dataFile=None,verbosity=1):
  if verbosity > 0:
    if printScript:
      thisScript = sys.argv[0]                                    # get name of script
      print(mcol.func+thisScript+mcol.clear+": ",end='')

    if type(value) is str:
      valueStr = value
    else:
      valueStr = toPrecision(value,precision)
    
    if error is None:
      print(mcol.varName+name+mcol.clear
            +" = "+valCol+valueStr+mcol.clear
            +mcol.varType+" "+unit+mcol.clear,flush=True,end=end)
    else:
      errorStr = toPrecision(error,errorPrecision)
      print(mcol.varName+name+mcol.clear
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
  if printScript:
    thisScript = sys.argv[0]                                    # get name of script
    print(mcol.func+thisScript+mcol.clear+": ",end='')
  print(mcol.warning+"Warning: "+string,end='')
  if code is not None: 
    print(" [code="+str(code)+"]",end='')
  print(mcol.clear,flush=True,end=end)

def errorOut(string,printScript=False,fatal=False,code=None,end="\n"):
  if printScript:
    thisScript = sys.argv[0]                                    # get name of script
    print(mcol.func+thisScript+mcol.clear+": ",end='')
  if fatal:
    prefix = "Fatal Error: "
  else:
    prefix = "Error: "
  print(mcol.error+prefix+string+mcol.error,end='')
  if code is not None: 
    print(" [code="+str(code)+"]")
  print(mcol.clear,flush=True,end=end)
  if fatal: exit()

def successOut(string,printScript=False,prefix=None,end="\n"):
  if printScript:
    thisScript = sys.argv[0]                                    # get name of script
    print(mcol.func+thisScript+mcol.clear+":",end=' ')
  if prefix is not None:
    print(mcol.success+prefix,end=' ')
  print(mcol.success+string+mcol.clear,flush=True,end=end)
