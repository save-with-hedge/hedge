import logging

from utils.path_anchor import PROJECT_ROOT


def get_logger():
    # return logging.getLogger("gunicorn.error")
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logger.propagate = False
    path = str(PROJECT_ROOT) + "/logs/python.log"
    if len(logger.handlers) == 0:
        handler = logging.FileHandler(path)
        handler.setLevel(logging.INFO)
        handler.setFormatter(
            logging.Formatter(
                "[%(asctime)s] %(name)s [%(levelname)s] - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
            )
        )
        logger.addHandler(handler)
    return logger


if __name__ == "__main__":
    logger = get_logger()
    logger.info("This is a test")
