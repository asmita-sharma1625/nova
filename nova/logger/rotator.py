#!/usr/bin/python

import os
import time
from common.singleton import SingletonProcess
import sys
import shutil

class Rotator:

  def rotate_log_file(self):
      map (self.__rotate_file, self.__file_lists())

  fileextension = "metric.log"
  def __init__(self,path):
    self.path = path
    
  #Double underscore for private method
  def __rotate_file(self, filename):
    timestamp = long(time.time())
    newfilename = filename +"."+ str(timestamp)
    os.rename(filename, newfilename)
    self.__create_blankfile(filename)

  def __file_lists(self):
      #Below is the list comprehension to iterate on the files inside the directory. It will give the list of nested directory also matching the file extension
      return [os.path.join(dirpath, files) \
                for (dirpath, dirname, filename) in os.walk(self.path) \
                for files in filename if files.endswith(Rotator.fileextension)]

  def __create_blankfile(self, filename):
    open(filename, "a").close()

'''
  This rotator.py can be directly called to run the rotator. In future, this code may be moved somewhere else.
'''
#if __name__ == "main":
if len(sys.argv) < 2:
  sys.stderr.write("Logfile path is not provided\n")
  exit(-2)

if len(sys.argv) > 2:
  sys.stderr.write("Extra arguments will be ignored\n")
singleton = SingletonProcess("jio-rotator")
singleton.checkSingleton()

#If it reaches here, it means there is only one process running
logrotator = Rotator(sys.argv[1])
print sys.argv[1]
logrotator.rotate_log_file()

