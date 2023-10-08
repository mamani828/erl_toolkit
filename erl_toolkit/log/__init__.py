import logging

import colorama
import colorlog
from erl_toolkit.log.tqdm_stream import TqdmStream
from erl_toolkit.log.exit_handler import ExitHandler

__all__ = ["get_logger"]

colorama.init()
loggers = {}


def get_logger(name: str, level=logging.DEBUG, exit_on_error=True):
    global loggers
    if name in loggers:
        return loggers[name]

    fmt = (
        f"%(log_color)s[%(process)d][%(asctime)s]"
        f"[%(levelname)s: %(name)s: %(lineno)4d]: %(message)s"
    )
    handler = colorlog.StreamHandler(stream=TqdmStream)
    handler.setFormatter(colorlog.ColoredFormatter(fmt))

    logger = colorlog.getLogger(name)
    logger.addHandler(handler)
    logger.setLevel(level)
    if exit_on_error:
        handler = ExitHandler(stream=TqdmStream)
        handler.setFormatter(colorlog.ColoredFormatter(fmt))
        logger.addHandler(handler)
    logger.propagate = False
    loggers[name] = logger
    return logger
