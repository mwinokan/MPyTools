
import mcol # https://github.com/mwinokan/MPyTools
import mout # https://github.com/mwinokan/MPyTools

# import matplotlib
# matplotlib.use("tkagg")
import matplotlib.pyplot as plt

import numpy as np
import string

def fit(xdata,ydata,rank=0,verbosity=1,printScript=False,title="",fitMin=None,fitMax=None,precision=4,errorPrecision=2,xUnit="",yUnit="",dataFile=None):

  # if there are nested ydatas:
  many = any(isinstance(el,list) for el in ydata)

  if xdata is None:
    if many:
      xdata = [ i for i in range(len(ydata[0])) ]
    else:
      xdata = [ i for i in range(len(ydata)) ]

  if title is None: title = ""

  # initialise arrays
  combined_xdata=[]
  combined_ydata=[]
  combined_data=[]

  # check if multiple ydata sets
  if not many:
    # if just one set of data
    for index,xpoint in enumerate(xdata):
      if fitMin is not None and xpoint < fitMin:
        continue
      if fitMax is not None and xpoint > fitMax:
        break
      combined_xdata.append(xpoint)
      combined_ydata.append(ydata[index])
  else:
    # loop over ydata sets
    for data in ydata:
      for index,ypoint in enumerate(data):
        if fitMin is not None and xdata[index] < fitMin:
          continue
        if fitMax is not None and xdata[index] > fitMax:
          break
        combined_xdata.append(xdata[index])
        combined_ydata.append(ypoint)
  
  # get the number of datapoints
  num_points=len(combined_ydata)

  # user output
  if verbosity > 0:
    mout.out("fitting "+
             mcol.varName+title+mcol.clear+
             " (rank "+str(rank)+", "+
             str(num_points)+" points) "+
             mcol.clear+"...",
             printScript=printScript,end=' ')
    if fitMin is not None or fitMax is not None:
      mout.out("fitrange=["+str(fitMin)+":"+str(fitMax)+"]",
               printScript=False,end=' ')


  # the actual fitting:
  coeffs,variance = np.polyfit(combined_xdata,combined_ydata,rank,cov=True)

  # user output
  if verbosity > 0:
    mout.out("Done.")

  # get list of letters in the alphabet
  alphabet_string = string.ascii_uppercase
  # alphabet_string = string.ascii_lowercase
  alphabet_list = list(alphabet_string)

  # write out the function type:
  if verbosity > 1:
    mout.out(mcol.func+"f"+mcol.clear+"("+mcol.arg+"x"+mcol.clear+") = ",end='')
    for i in range(rank,-1,-1):
      if i == 0:
        x_string = " "
      elif i == 1:
        x_string = mcol.arg+"x"+mcol.clear+" + "
      else:
        x_string = mcol.arg+"x^"+str(i)+mcol.clear+" + "
      mout.out(mcol.varName+alphabet_list[rank-i]+x_string+mcol.clear,end='')
    mout.out("")

  # initialise arrays
  vals=[]
  errs=[]

  # process the coefficients
  for i in range(rank,-1,-1):
    # append the current coefficient
    vals.append(coeffs[i])
    errs.append(np.sqrt(variance[i,i]))

  if yUnit != "" and xUnit != "":
    for i in range(rank,-1,-1):
      # write out the results
      unitString=yUnit
      if i == 1:
        unitString = unitString+"/("+xUnit+")"
      elif i > 1:
        unitString = unitString+"/("+xUnit+"^"+str(i)+")"
      mout.varOut(alphabet_list[rank-i],vals[i],unit=unitString,error=errs[i],valCol=mcol.result,precision=precision,errorPrecision=errorPrecision,printScript=printScript,dataFile=dataFile,verbosity=verbosity)

  # get the resulting fit function
  fit_func = np.poly1d(coeffs)

  if rank == 0:
    vals=vals[0]
    errs=errs[0]

  # return the necessary
  return vals, errs, fit_func

def getCoeffStr(vals,errs,order,xUnit="",yUnit="",precision=4,errorPrecision=2):

  try:
    rank = len(vals)
    is_rank0=False
  except:
    rank = 0
    is_rank0=True

  unitString=yUnit
  if order == 1:
    unitString = unitString+"/("+xUnit+")"
  elif order > 1:
    unitString = unitString+"/("+xUnit+"^"+str(order)+")"
  
  if not is_rank0:
    valueStr = mout.toPrecision(vals[rank-order],precision)
    errorStr = mout.toPrecision(errs[rank-order],errorPrecision)
  else:
    valueStr = mout.toPrecision(vals,precision)
    errorStr = mout.toPrecision(errs,precision)

  string = valueStr + " +/- " + errorStr + " " + unitString

  return string
