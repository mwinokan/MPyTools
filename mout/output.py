import mcol
import sys                                    # sys.argv
import math

def out(string,printScript=False,end="\n"):
  if printScript:
    thisScript = sys.argv[0]                                    # get name of script
    print(mcol.func+thisScript+mcol.clear+": ",end='')
  print(string+mcol.clear,flush=True,end=end)

def varOut(name, value, unit="",valCol="",precision=8,printScript=False,end="\n"):
  if printScript:
    thisScript = sys.argv[0]                                    # get name of script
    print(mcol.func+thisScript+mcol.clear+": ",end='')
  valueStr = toPrecision(value,precision)
  print(mcol.varName+name+mcol.clear
        +" = "+valCol+valueStr+mcol.clear
        +mcol.varType+" "+unit+mcol.clear,flush=True,end=end)

def warningOut(string,printScript=False,code=None,end="\n"):
  if printScript:
    thisScript = sys.argv[0]                                    # get name of script
    print(mcol.func+thisScript+mcol.clear+": ",end='')
  print(mcol.warning+"Warning: "+string,end='')
  if code is not None: 
    print(" [code="+str(code)+"]")
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

def toPrecision(x,p):
    """
    returns a string representation of x formatted with a precision of p

    Based on the webkit javascript implementation taken from here:
    https://code.google.com/p/webkit-mirror/source/browse/JavaScriptCore/kjs/number_object.cpp
    """

    x = float(x)

    if x == 0.:
        return "0." + "0"*(p-1)

    out = []

    if x < 0:
        out.append("-")
        x = -x

    e = int(math.log10(x))
    tens = math.pow(10, e - p + 1)
    n = math.floor(x/tens)

    if n < math.pow(10, p - 1):
        e = e -1
        tens = math.pow(10, e - p+1)
        n = math.floor(x / tens)

    if abs((n + 1.) * tens - x) <= abs(n * tens -x):
        n = n + 1

    if n >= math.pow(10,p):
        n = n / 10.
        e = e + 1

    m = "%.*g" % (p, n)

    if e < -2 or e >= p:
        out.append(m[0])
        if p > 1:
            out.append(".")
            out.extend(m[1:p])
        out.append('e')
        if e > 0:
            out.append("+")
        out.append(str(e))
    elif e == (p -1):
        out.append(m)
    elif e >= 0:
        out.append(m[:e+1])
        if e+1 < len(m):
            out.append(".")
            out.extend(m[e+1:])
    else:
        out.append("0.")
        out.extend(["0"]*-(e+1))
        out.append(m)

    return "".join(out)
