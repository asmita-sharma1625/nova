import time
import socket
from nova.logger.common.configReader import ConfigReader 
from nova.logger.common import configWriter

'''
	Declares constants.
'''
class Constants:

  #LOGDIR = ConfigReader.getValue("Constants", "LogDir")
  #FILENAME = ConfigReader.getValue("Constants", "Filename")
  #SOCKET = ConfigReader.getValue("Constants", "Socket")
  RUNTIME = "Runtime"
  FAILCOUNT = "Failure Count"
# Use constants for metric type 
  METRIC_TYPE = "Metric Type"
  METRIC_NAME = "Name"
  REGION = "Region"
  ZONE = "Zone"
  HOST = "Host"
  SERVICE = "Service"
  TIME = "Timestamp"
  SEPARATOR = " : "
  DELIMITER = "\n"

  @staticmethod
  def setLogDir(logdir):
    configWriter.updateConfigFile("Constants", "LogDir", logdir)

  @staticmethod
  def getLogDir():
    return ConfigReader.getValue("Constants", "LogDir")

  @staticmethod
  def getFilename():
    return ConfigReader.getValue("Constants", "Filename")

  @staticmethod
  def getSocket():
    return ConfigReader.getValue("Constants", "Socket")

  '''
    Get host from metadata.
  '''
  @staticmethod
  def getHostname():
      return socket.gethostname()

  @staticmethod
  def getServiceName():
    return ConfigReader.getValue("Constants", "Service")

  @staticmethod
  def toStringCommon (service):
    return Constants.HOST + Constants.SEPARATOR + Constants.getHostname() + Constants.DELIMITER + Constants.SERVICE + Constants.SEPARATOR + service + Constants.DELIMITER 

  @staticmethod
  def appendTimestamp (string):
    return string + Constants.TIME + Constants.SEPARATOR + `time.time()` + Constants.DELIMITER

  @staticmethod
  def toStringRuntime (name, mType, runtime):
    return Constants.appendTimestamp(Constants.METRIC_NAME + Constants.SEPARATOR + name + Constants.DELIMITER + Constants.METRIC_TYPE + Constants.SEPARATOR + mType + Constants.DELIMITER + Constants.RUNTIME + Constants.SEPARATOR + `runtime` + Constants.DELIMITER)

  @staticmethod
  def toStringCount (name, mType, count):
    return Constants.appendTimestamp(Constants.METRIC_NAME + Constants.SEPARATOR + name + Constants.DELIMITER + Constants.METRIC_TYPE + Constants.SEPARATOR + mType + Constants.DELIMITER + Constants.FAILCOUNT + Constants.SEPARATOR + `count` + Constants.DELIMITER)


