
import mout
import mcol

def write2file(filename,string,verbosity=0):
  output = open(filename,'w')
  output.write(string)
  output.write('\n')
  output.close()
  if verbosity > 0:
  	mout.out("Line written to "+mcol.file+filename)

def append2file(filename,string,verbosity=0):
  output = open(filename,'a')
  output.write(string)
  output.write('\n')
  output.close()
  if verbosity > 0:
  	mout.out("Line written to "+mcol.file+filename)
