from nova.logger.logger import Logger

logger = None

def setLogger(service, configFile):
    global logger
    logger  = Logger(service, configFile)

#TODO :  make changes for logIfFAil 
def LogIfFail(name, metricType, expectedReturn, counter):
    def real_decorator(function):
        def wrapper(*args, **kwargs):
            return logger.logIfFail(name, metricType, expectedReturn, counter, function, *args, **kwargs)
        return wrapper
    return real_decorator

def ReportLatency(name, metricType):
    def real_decorator(function):
        def wrapper(*args, **kwargs):
           return logger.reportLatency(name, metricType, function, *args, **kwargs)
        return wrapper
    return real_decorator

