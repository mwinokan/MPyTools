
def append2file(filename,string,verbosity=1):
  output = open(filename,'a')
  output.write(string)
  output.write('\n')
  output.close()
