import mcol
import sys                                    # sys.argv

def out(string,printScript=False,end="\n"):
  if printScript:
    thisScript = sys.argv[0]                                    # get name of script
    print(mcol.func+thisScript+mcol.clear+": ",end='')
  print(string+mcol.clear,flush=True,end=end)

def varOut(name, value, unit="",valCol="",printScript=False,end="\n"):
  if printScript:
    thisScript = sys.argv[0]                                    # get name of script
    print(mcol.func+thisScript+mcol.clear+": ",end='')
  print(mcol.varName+name+mcol.clear
        +" = "+valCol+f"{value}"+mcol.clear
        +mcol.varType+" "+unit+mcol.clear,flush=True,end=end)
