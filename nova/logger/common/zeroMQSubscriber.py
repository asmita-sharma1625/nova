from logbook.queues import ZeroMQSubscriber
from logbook import TimedRotatingFileHandler
from nova.logger.common.Constants import Constants
import zmq

class MyZeroMQSubscriber:

  def __init__(self):
    try:
      print "subscriber initiated"
      self.subscriber = ZeroMQSubscriber(Constants.getSocket(), multi = True)
    except zmq.error.ZMQError:
      raise Exception("Subscriber process already running")

  def startSubscriber(self, filepath):
    print "subscriber started"
    with TimedRotatingFileHandler(filepath, date_format='%Y-%m-%d %H:%M'):
      print "received log", self.subscriber.recv()
      self.subscriber.dispatch_forever()

