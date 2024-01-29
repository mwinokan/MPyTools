
import mcol
import logging
import logging.config
import haggis.logs

# VAR?

def setup_logger(name):
  
  logger = logging.getLogger(name)

  logging.config.dictConfig(LOG_CONFIG)
  logging.basicConfig(level="DEBUG")

  return logger

haggis.logs.add_logging_level('VAR',22)
haggis.logs.add_logging_level('TITLE',33)
haggis.logs.add_logging_level('HEADER',32)
haggis.logs.add_logging_level('SUCCESS',31)
haggis.logs.add_logging_level('OUT',21)
haggis.logs.add_logging_level('READING',11)
haggis.logs.add_logging_level('WRITING',12)

class WarningFilter(logging.Filter):
    def filter(self, record: logging.LogRecord):
        return record.levelno == logging.WARNING
    
class InfoFilter(logging.Filter):
    def filter(self, record: logging.LogRecord):
        return record.levelno == logging.INFO
    
class ErrorFilter(logging.Filter):
    def filter(self, record: logging.LogRecord):
        return record.levelno >= logging.ERROR

class SuccessFilter(logging.Filter):
    def filter(self, record: logging.LogRecord):
        return record.levelno == logging.SUCCESS
    
class DebugFilter(logging.Filter):
    def filter(self, record: logging.LogRecord):
        return record.levelno == logging.DEBUG

class HeaderFilter(logging.Filter):
    def filter(self, record: logging.LogRecord):
        return record.levelno == logging.HEADER

class TitleFilter(logging.Filter):
    def filter(self, record: logging.LogRecord):
        return record.levelno == logging.TITLE

class DebugFilter(logging.Filter):
    def filter(self, record: logging.LogRecord):
        return record.levelno == logging.DEBUG

class InfoFilter(logging.Filter):
    def filter(self, record: logging.LogRecord):
        return record.levelno == logging.INFO

class OutFilter(logging.Filter):
    def filter(self, record: logging.LogRecord):
        return record.levelno == logging.OUT

class ReadingFilter(logging.Filter):
    def filter(self, record: logging.LogRecord):
        return record.levelno == logging.READING

class WritingFilter(logging.Filter):
    def filter(self, record: logging.LogRecord):
        return record.levelno == logging.WRITING

LOG_CONFIG = {
  "version": 1,
  "disable_existing_loggers": False,
  "formatters": {
    "default": {"format": f" %(levelname)s >%(message)s< NOT IMPLEMENTED"},
    
    "reading": { "format": f"{mcol.inverse}{mcol.bold}{mcol.file} DISK {mcol.clear} Reading {mcol.file}%(message)s{mcol.clear}"},
    "writing": { "format": f"{mcol.inverse}{mcol.bold}{mcol.file} DISK {mcol.clear} Writing {mcol.file}%(message)s{mcol.clear}"},

    "warning": { "format": f"{mcol.inverse}{mcol.warning}{mcol.bold} Warning {mcol.clear}{mcol.warning} %(message)s{mcol.clear}"},
    "error": { "format": f"{mcol.inverse}{mcol.error} %(levelname)s {mcol.clear}{mcol.error} %(message)s!{mcol.clear}"},
    "success": { "format": f"{mcol.inverse}{mcol.success} SUCCESS {mcol.clear}{mcol.success} %(message)s!{mcol.clear}"},
    "header": { "format": f"{mcol.bold}{mcol.orange}%(message)s{mcol.clear}"},
    "title": { "format": f"{mcol.blue}{mcol.bold}>>> %(message)s{mcol.clear}"},

    "debug": { "format": f"{mcol.faint}DEBUG: %(message)s{mcol.clear}"},
    "info": { "format": f"%(message)s"},
  },

  "filters": {
    "warning": {
      "()": WarningFilter
    },
  "info": {
      "()": InfoFilter
    },
    "error": {
      "()": ErrorFilter
    },
    "success": {
      "()": SuccessFilter
    },
    "header": {
      "()": HeaderFilter
    },
    "title": {
      "()": TitleFilter
    },
    "debug": {
      "()": DebugFilter
    },
    "out": {
      "()": OutFilter
    },
    "reading": {
      "()": ReadingFilter
    },
    "writing": {
      "()": WritingFilter
    },
  },
  "handlers": {

    "default": {
      "class": "logging.StreamHandler",
      "formatter": "default",
      "stream": "ext://sys.stdout",
    },
    "warning": {
      "class": "logging.StreamHandler",
      "formatter": "warning",
      "stream": "ext://sys.stdout",
      "filters": [ "warning" ],
    },
    "error": {
      "class": "logging.StreamHandler",
      "formatter": "error",
      "stream": "ext://sys.stdout",
      "filters": [ "error" ],
    },
    "success": {
      "class": "logging.StreamHandler",
      "formatter": "success",
      "stream": "ext://sys.stdout",
      "filters": [ "success" ],
    },
    "header": {
      "class": "logging.StreamHandler",
      "formatter": "header",
      "stream": "ext://sys.stdout",
      "filters": [ "header" ],
    },
    "title": {
      "class": "logging.StreamHandler",
      "formatter": "title",
      "stream": "ext://sys.stdout",
      "filters": [ "title" ],
    },
    "debug": {
      "class": "logging.StreamHandler",
      "formatter": "debug",
      "stream": "ext://sys.stdout",
      "filters": [ "debug" ],
    },
    "info": {
      "class": "logging.StreamHandler",
      "formatter": "info",
      "stream": "ext://sys.stdout",
      "filters": [ "info" ],
    },
    "out": {
      "class": "logging.StreamHandler",
      "formatter": "info",
      "stream": "ext://sys.stdout",
      "filters": [ "out" ],
    },
    "reading": {
      "class": "logging.StreamHandler",
      "formatter": "reading",
      "stream": "ext://sys.stdout",
      "filters": [ "reading" ],
    },
    "writing": {
      "class": "logging.StreamHandler",
      "formatter": "writing",
      "stream": "ext://sys.stdout",
      "filters": [ "writing" ],
    },
  },
  "loggers": {
    "root": {
      "level": "DEBUG", 
      "handlers": [ "warning", "error", "success", "header", "title", "debug", "info", "out", "reading", "writing" ]
    }
  }
}
