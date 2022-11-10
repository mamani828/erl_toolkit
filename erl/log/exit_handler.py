import colorlog
import sys
import logging


class ExitHandler(colorlog.StreamHandler):
    def emit(self, record):
        if record.levelno >= logging.ERROR:
            super(ExitHandler, self).emit(record)
            sys.exit(1)
