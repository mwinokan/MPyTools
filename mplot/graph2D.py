
import mcol # https://github.com/mwinokan/MPyTools
import mout # https://github.com/mwinokan/MPyTools

# matplotlib.use("tkagg")

import matplotlib as mpl
import os
if "scarf" in os.popen("hostname").read():
  if not "ui3" in os.popen("hostname").read():
    # print("Using agg for Matplotlib")
    mpl.use('agg')

import matplotlib.pyplot as plt

import numpy as np

"""

  To-Do's
    * Close after saving argument?

"""

def graph2D(xdata,ydata,
            fitFunc=None,
            printScript=False,
            ytitles=None,fitTitle=None,
            style=None,
            filename=None,
            show=True,
            xmin=None,xmax=None,
            ymin=None,ymax=None,
            xlab='x',ylab='y',
            title=None,
            subtitle=None,
            verbosity=2,
            colour=None,
            yerrors=None,xerrors=None,
            alpha=1.0,
            xticrot=None,xticsize=None,
            xSci=False,ySci=False,
            xLog=False,yLog=False,
            dpi=100,figsize=[6.4, 4.8],bar_width=0.8,zeroaxis=False):

  # graph = plt.figure(dpi=dpi,figsize=figsize)
  graph, axis = plt.subplots(dpi=dpi,figsize=figsize)

  if (verbosity > 0):
    if title is not None:
      mout.out("graphing "+mcol.varName+
               title+
               mcol.clear+" ... ",
               printScript=printScript,
               end='')
    else:
      mout.out("graphing ... ",
               printScript=printScript,
               end='')

  many = any(isinstance(el,list) for el in ydata)

  # plot the normal data
  if many:
    # ydata is a list of lists!
    if ytitles is not None:
      # for curve, label in zip(ydata,ytitles):
      for index, curve in enumerate(ydata):

        # print("many!")

        if ytitles[index] is None:
          label = "ydata["+str(index)+"]"
        else:
          label = ytitles[index]

        if style is None or style[index] is None:
          if colour is None or colour[index] is None:
            plt.plot(xdata,curve,label=label)
          else:
            plt.plot(xdata,curve,colour[index],label=label)
        elif style[index] == "bar":
          if colour is None or colour[index] is None:
            plt.bar(xdata,curve,align='center',label=label,alpha=alpha)
          else:
            plt.bar(xdata,curve,align='center',label=label,color=colour[index],alpha=alpha)
        else:
          if colour is None or colour[index] is None:
            plt.plot(xdata,curve,style[index],label=label)
          else:
            plt.plot(xdata,curve,colour[index]+style[index],label=label)
    else:
      for index, curve in enumerate(ydata):
        if style is None or style[index] is None:
          if colour is None or colour[index] is None:
            plt.plot(xdata,curve,label="ydata["+str(index)+"]")
          else:
            plt.plot(xdata,curve,colour[index],label="ydata["+str(index)+"]")
        elif style[index] == "bar":
          if colour is None or colour[index] is None:
            plt.bar(xdata,curve,align='center',label="ydata["+str(index)+"]",alpha=alpha)
          else:
            plt.bar(xdata,curve,colour[index],align='center',label="ydata["+str(index)+"]",alpha=alpha)
        else:
          if colour is None or colour[index] is None:
            plt.plot(xdata,curve,style[index],label="ydata["+str(index)+"]")
          else:
            plt.plot(xdata,curve,colour[index]+style[index],label="ydata["+str(index)+"]")

  else: 
    if ytitles is not None:
      label = ytitles
      print(label)
    else:
      label = None
    if colour is None:
      colour = "k"
      alpha = 0.5
    # ydata is just a list!
    if label is not None:
      if style is None:
        plt.plot(xdata,ydata,colour,label=label)
      elif style == "bar":
        plt.bar(xdata,ydata,color=colour,label=label,align='center',alpha=alpha,width=bar_width)
      else:
        plt.plot(xdata,ydata,colour+style,label=label)
    else:
      if style is None:
        plt.plot(xdata,ydata,colour)
      elif style == "bar":
        plt.bar(xdata,ydata,color=colour,align='center',alpha=alpha,width=bar_width)
      else:
        plt.plot(xdata,ydata,colour+style)

  if xSci:
    plt.ticklabel_format(axis='x',style='sci',scilimits=(0,0))
  if ySci:
    plt.ticklabel_format(axis='y',style='sci',scilimits=(0,0))

  # plot the yerrorbars
  if yerrors is not None:
    if many:
      for index, curve in enumerate(ydata):
        if yerrors[index] is not None:
          if style == "bar":
            this_colour = "k"
          if colour is None or colour[index] is None:
            this_colour = None
          else:
            this_colour = colour[index]

          if colour is None or colour[index] is None:
            plt.errorbar(xdata,curve,yerrors[index],fmt='none',capsize=3,capwidth=2,color='C'+str(index))
          else:
            plt.errorbar(xdata,curve,yerrors[index],fmt='none',capsize=3,capwidth=2,color=colour[index])

    else:
      if style == "bar":
        colour = "k"
      if colour is None:
        plt.errorbar(xdata,ydata,yerrors,fmt='none',capsize=3,capwidth=2,color='C'+str(index),colour="k")
      else:
        plt.errorbar(xdata,ydata,yerrors,fmt='none',color=colour,capsize=3,capwidth=2)
  # plot the xerrorbars
  if xerrors is not None:
    if many:
      for index, curve in enumerate(ydata):
        if xerrors[index] is not None:
          if style == "bar":
            this_colour = "k"
          if colour is None or colour[index] is None:
            this_colour = None
          else:
            this_colour = colour[index]

          if colour is None or colour[index] is None:
            plt.errorbar(xdata,curve,xerr=xerrors[index],fmt='none',capsize=3,capwidth=2,color='C'+str(index))
          else:
            plt.errorbar(xdata,curve,xerr=xerrors[index],fmt='none',capsize=3,capwidth=2,color=colour[index])

    else:
      if style == "bar":
        colour = "k"
      if colour is None:
        plt.errorbar(xdata,ydata,xerr=xerrors,fmt='none',capsize=3,capwidth=2,color='C'+str(index))
      else:
        plt.errorbar(xdata,ydata,xerr=xerrors,fmt='none',color=colour,capsize=3,capwidth=2)

  # plot the fitting function
  if fitFunc is not None:
    if fitTitle is None:
      plt.plot(xdata,fitFunc(xdata),'k--',label="f(x) "+str(fitFunc))
    else:
      plt.plot(xdata,fitFunc(xdata),'k--',label=fitTitle)

  plt.axis([xmin,xmax,ymin,ymax])
  plt.xlabel(xlab)
  plt.ylabel(ylab)
  plt.suptitle(title)

  if zeroaxis:
    axis.axhline(y=0, color='k')
    axis.axvline(x=0, color='k')

  if xLog:
    plt.xscale('log')
  if yLog:
    plt.yscale('log')

  if xticrot != None:
    plt.xticks(rotation=xticrot)

  if xticsize != None:
    plt.xticks(fontsize=xticsize)

  if subtitle is not None:
    plt.figtext(0.5,0.91,subtitle,horizontalalignment='center')

  if many or ytitles is not None:
    plt.legend()

  if show:
    if (verbosity > 1):
      mout.out("showing ... ",end='')
    plt.show()

  if filename is not None:
    if (verbosity > 0):
      mout.out("saving as " + mcol.file + filename + mcol.clear + " ... ",end='')
    plt.savefig(filename)
    plt.close(fig=graph)
  
  if (verbosity > 0):
    mout.out("Done.")

def chart2D(xdata,ydata,fitFunc=None,printScript=False,ytitles=None,fitTitle=None,style=None,filename=None,show=True,xmin=None,xmax=None,ymin=None,ymax=None,xlab='x',ylab='y',title=None,verbosity=2,subtitle=None,colour=None,yerrors=None,xerrors=None,alpha=1.0,xticrot=None,xticsize=None,xSci=False,ySci=False,bar_width=0.8):

  many = any(isinstance(el,list) for el in ydata)

  if style is None and not many:
    style = "bar"

  graph2D(xdata,ydata,fitFunc=fitFunc,printScript=printScript,ytitles=ytitles,fitTitle=fitTitle,style=style,filename=filename,show=show,xmin=xmin,xmax=xmax,ymin=ymin,ymax=ymax,xlab=xlab,ylab=ylab,title=title,verbosity=verbosity,subtitle=subtitle,colour=colour,yerrors=yerrors,xerrors=xerrors,alpha=alpha,xticrot=xticrot,xticsize=xticsize,ySci=ySci,bar_width=bar_width)
