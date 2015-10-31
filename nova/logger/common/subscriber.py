import sys
import os
import socket
from logbook.queues import ZeroMQSubscriber
from logbook import TimedRotatingFileHandler
from nova.logger.common import Constants
from logger.common.configReader import ConfigReader

ConfigReader.setConfig(sys.argv[1])

mySocket = ConfigReader.getValue("Constants", "Socket")
subscriber = ZeroMQSubscriber(mySocket)

filepath = os.path.join(os.path.join(ConfigReader.getValue("Constants", "LogDir"), os.path.join(socket.gethostname(), os.path.join(ConfigReader.getValue("Constants", "Service"), ConfigReader.getValue("Constants", "Filename")))))

with TimedRotatingFileHandler(filepath, date_format='%Y-%m-%d %H:%M'):
  print subscriber.recv().message
  subscriber.dispatch_forever()

