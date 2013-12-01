from database import Database

class Logger:
    gag_id = None
    def __init__(self):
        self._db = Database()

    def error(self):
        if Logger.gag_id:
            self._db.err_gag(Logger.gag_id)

