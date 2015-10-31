'''
	Declares constants.
'''
class Constants:

	LOGDIR = "/var/logs/compute/"
	FILENAME = "metric.log"
	RUNTIME = "Runtime"
	FAILCOUNT = "Failure Count"
	# Use constants for metric type 
	METRIC_TYPE = "Metric Type"
	METRIC_NAME = "Name"
	REGION = "Region"
	ZONE = "Zone"
	HOST = "Host"
	SERVICE = "Service"
	SEPARATOR = " : "
	DELIMITER = "\n"

  @staticmethod
  def toStringCommon (region, zone, host, service):
    return Constants.REGION  + Constants.SEPARATOR + region + Constants.DELIMITER + Constants.ZONE + Constants.SEPARATOR + zone + Constants.DELIMITER + Constants.HOST + Constants.SEPARATOR + host + Constants.DELIMITER + Constants.SERVICE + Constants.SEPARATOR + service + Constants.DELIMITER

  @staticmethod
  def toStringRuntime (name, mType, runtime):
    return Constants.METRIC_NAME + Constants.SEPARATOR + name + Constants.DELIMITER + Constants.METRIC_TYPE + Constants.SEPARATOR + mType + Constants.DELIMITER + Constants.RUNTIME + Constants.SEPARATOR + `runtime` + Constants.DELIMITER

  @staticmethod
  def toStringCount (name, mType, count):
    return Constants.METRIC_NAME + Constants.SEPARATOR + name + Constants.DELIMITER + Constants.METRIC_TYPE + Constants.SEPARATOR + mType + Constants.DELIMITER + Constants.FAILCOUNT + Constants.SEPARATOR + `count` + Constants.DELIMITER
	

