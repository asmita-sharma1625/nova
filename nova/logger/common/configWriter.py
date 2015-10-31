import ConfigParser

filename = None

def CreateConfigFile(filepath, section, key, value):
  global filename
  filename = filepath
  config = ConfigParser.RawConfigParser()
  #print "create config filename : "+ filename

  # When adding sections or items, add them in the reverse order of
  # how you want them to be displayed in the actual file.
  # In addition, please note that using RawConfigParser's and the raw
  # mode of ConfigParser's respective set functions, you can assign
  # non-string values to keys internally, but will receive an error
  # when attempting to write to a file or when you get it in non-raw
  # mode. SafeConfigParser does not allow such assignments to take place.
  

  config.add_section(section)
  config.set(section, key, value)
  
  # check if this config already exsits in file
  #try:
  #  configRead = ConfigParser.SafeConfigParser()
  #  configRead.read(filepath)
  #  configRead.get(section, key)
  #except:
    # Writing our configuration file to input filename
  #  with open(filepath, 'a') as configfile:
  #    config.write(configfile)
  #    sys.exit(0)
  
  #configRead.remove_option(section, key)
  # Writing our configuration file to input filename
  with open(filepath, 'a') as configfile:
    config.write(configfile)

def setConfigFile(filepath):
  global filename 
  filename = filepath
  #print "filename : "+ filename

def updateConfigFile(section, key, value):
  global filename
  CreateConfigFile(filename, section, key, value)
