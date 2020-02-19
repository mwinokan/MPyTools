import os
def module(command,*arguments):
  command = os.popen('/usr/share/lmod/lmod/libexec/lmod python %s %s' % (command,' '.join(arguments))).read()
  exec(command)
