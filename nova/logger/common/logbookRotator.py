from logbook.handlers import TimedRotatingFileHandler

class rotator(TimedRotatingFileHandler): 
  def perform_rollover(self):
        if self.backup_count > 0:
            for time, filename in self.files_to_delete():
                os.remove(filename)
        self._open('w')
