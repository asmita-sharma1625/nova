# Initialize logger to log monitor events

from logger.common.handler import Handler
import sys

sys.path.append('/home/asmi/monitor-common/logger')

class monitorLog:
  
  logger = Handler("monitor").getLogHandler()

  def logInfo(self, msg):
    logger.info(msg)

  def logError(self, msg):
    logger.error(msg)
