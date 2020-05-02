import os
import mout

from module import isEureka

def module(command,*arguments):
  global isEureka
  if isEureka:
    command = os.popen('/usr/share/lmod/lmod/libexec/lmod python %s %s' % (command,' '.join(arguments))).read()
    exec(command)
    return 0
  else:
    mout.warningOut("Not on EUREKA! Not loading module.")
    return 1
