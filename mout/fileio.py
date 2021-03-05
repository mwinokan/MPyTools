
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

def array2file(filename,list_of_things,append=False,verbosity=1):
  if append:
    output = open(filename,'a')
  else:
    output = open(filename,'w')

  many = any(isinstance(el,list) for el in list_of_things)

  if many:
    counter=0
    for many_things in list_of_things:
      string=""
      for thing in many_things:
        string += str(thing)
        string += " "
      output.write(string)
      output.write('\n')
      counter+=1
    output.close()
    # mout.errorOut("Nested Lists Unsupported",fatal=True,code="mout.array2file")
  else:
    counter=0
    for thing in list_of_things:
      try:
        string = str(thing)
      except:
        mout.errorOut("Could not convert item to string.",code=counter,fatal=True)
      output.write(string)
      output.write('\n')
      counter+=1
    output.close()

  if verbosity > 0:
    mout.out(str(counter)+" lines written to "+mcol.file+filename)
