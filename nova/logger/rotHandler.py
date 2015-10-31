from logging import handlers

class Rotator(handlers.TimedRotatingFileHandler):
  def getFilesToDelete(self):
    return []
