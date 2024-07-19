# TODO use a separate log file for python logs
import logging


def get_logger():
    return logging.getLogger("gunicorn.error")
