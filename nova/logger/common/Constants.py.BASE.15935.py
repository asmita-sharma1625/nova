'''
	Declares constants.
'''
class Constants:

	FILENAME = "metric.log"
	RUNTIME = "Runtime"
	FAILCOUNT = "Failure Count"
	# Use constants for metric type 
	METRIC_TYPE = "Metric Type"
	METRIC_NAME = "Name"
	REGION = "Region"
	ZONE = "Availability Zone"
	HOST = "Host"
	SEPARATOR = Constants.SEPARATOR
	DELIMITER = "\n"

	@staticmethod
	def toStringCommon (region, zone, host):
		return Constants.REGION  + Constants.SEPARATOR + region + Constants.DELIMITER + Constants.ZONE + Constants.SEPARATOR + zone + Constants.DELIMITER + Constants.HOST + Constants.SEPARATOR + host + Constants.DELIMITER 

	@staticmethod
	def toStringRuntime(name, mType, runtime):
		return Constants.METRIC_NAME + Constants.SEPARATOR + name + Constants.DELIMITER + Constants.METRIC_TYPE + Constants.SEPARATOR + mtype + Constants.DELIMITER + Constants.RUNTIME + Constants.SEPARATOR + `runtime` + "\n"
	
	@staticmethod
        def toStringCount(name, mType, count):
                return Constants.METRIC_NAME + Constants.SEPARATOR + name + Constants.DELIMITER + Constants.METRIC_TYPE + Constants.SEPARATOR + mtype + Constants.DELIMITER + Constants.FAILCOUNT + Constants.SEPARATOR + `count` + Constants.DELIMITER
	

