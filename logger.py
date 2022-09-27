import logging
from functools import wraps
from typing import Any

logging.basicConfig(filename='qrg.log', filemode='w', 
                    format="[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s")


def log_unknown_exceptions(log_lvl: int) -> Any:
    """Logs unknown exceptions that occur in a function to a log file.
    """
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            try:
                result = func(*args, **kwargs)
                return result
            except Exception as e:
                if log_lvl == logging.DEBUG:
                    logging.debug(e)
                elif log_lvl == logging.INFO:
                    logging.info(e)
                elif log_lvl == logging.WARNING:
                    logging.warning(e)
                elif log_lvl == logging.ERROR:
                    logging.error(e)
                elif log_lvl == logging.CRITICAL:
                    logging.critical(e)
                else:
                    raise ValueError('Invalid log level provided for log_unknown_exceptions decorator.')
                return None
        return wrapper 
    return decorate
