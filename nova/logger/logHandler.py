import logging
import os
import socket
from nova.logger.common.Constants import Constants
from nova.logger.common.handler import Handler

class LogHandler:

  def __init__ (self, service, configFile):
    self.service = service
    self.handler = Handler(self.service, configFile)
    self.logger = self.handler.getLogHandler()
    # start queue subscriber for logging 
    self.handler.startQueueSubscriber()
    # get queue handler for logging
    self.queueHandler = self.handler.getQueueHandler()
    self.commonLog = Constants.toStringCommon(service)

  def appendLog (self, msg):
    try:
      with self.queueHandler:
        self.logger.info(self.commonLog+msg)
    except:
      pass

  def appendCountLog(self, name, metricType, count):
    msg = Constants.toStringCount(name, metricType, count)
    self.appendLog(msg)

  def appendTimeLog(self, name, metricType, runtime):
    msg = Constants.toStringRuntime(name, metricType, runtime)
    self.appendLog(msg)



