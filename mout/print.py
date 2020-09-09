
import sys
import os

# Disable
def blockPrint():
  sys.stdout = open(os.devnull, 'w')

def redirectPrint(filename):
  sys.stdout = open(filename,'w')

# Restore
def enablePrint():
  sys.stdout = sys.__stdout__
