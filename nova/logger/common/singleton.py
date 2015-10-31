import os
import sys
import atexit

class SingletonProcess:
  def __init__(self, filename):
    self.filename = filename

  def checkSingleton(self):
    lockfile = "/var/lock/"+self.filename+".lock"
    if os.path.isfile(lockfile):
      print("Failed to create lockfile. Is another instance already running?")
      sys.exit(-1)
    else:
      f=open(lockfile,'w')
      atexit.register(deletefile, lockfile)
      
def deletefile(filename):
  os.remove(filename)

