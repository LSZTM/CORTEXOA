import functools
import logging
import inspect
import traceback
import sys
from datetime import datetime



def log_decorator(fn):
    logger = logging.getLogger(fn.__module__)
    line_number = inspect.getsourcelines(fn)[1]
    module_name = inspect.getmodule(fn).__name__

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        now = datetime.now()
        logger.info(" " * 3 + f"{now} - Going to run the '{fn.__name__}' method (Module: {module_name}, Line: {line_number})")

        try:
            out = fn(*args, **kwargs)
            logger.info(" " * 3 + f"{now} - Done successfully running the '{fn.__name__}' method (Module: {module_name}, Line: {line_number})")
            return out
        
        except Exception as err:
            logger.error(f"\nError occurred in method '{fn.__name__}' (Module: {module_name}, Line: {line_number}):")
            logger.error(f"Error Type: {type(err).__name__}")
            logger.error(f"Error Message: {str(err)}")
            logger.error(f"Traceback:\n{traceback.format_exc()}")
            sys.exit(1)

    return wrapper
