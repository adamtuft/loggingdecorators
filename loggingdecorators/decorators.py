from functools import wraps
from typing import Union
import logging

loggerClass = logging.getLoggerClass()


def on_init(logger: Union[str, loggerClass]="logger", level=logging.DEBUG, logargs=True, depth=0):
    """
    When applied to a class or an __init__ method, decorate it with a wrapper which logs the __init__ call using the
    given logger at the specified level.

    If "logger" is a string, look up an attribute of this name in the initialised object and use it to log the message.
    Otherwise, assume "logger" is an instance of a logger from the logging library and use it to log the message.

    If logargs is True, the message contains the arguments passed to __init__.

    If the decorated class or __init__ method is to be nested inside other decorators, increase the depth argument by 1
    for each additional level of nesting in order for the messages emitted to contain the correct source file name &
    line number.
    """

    const_depth = 2
    total_depth = const_depth + depth

    def decorator(constructor):

        if not callable(constructor):
            raise TypeError(f"{constructor} does not appear to be callable.")

        is_class = isinstance(constructor, type)  # class itself was passed in

        if is_class:
            to_call = getattr(constructor, "__init__")
        else:
            to_call = constructor

        def init_wrapper(self, *args, **kwargs):

            to_call(self, *args, **kwargs)

            _logger = getattr(self, logger) if isinstance(logger, str) else logger

            if not isinstance(_logger, loggerClass):
                raise TypeError(f"logger argument had unexpected type {type(_logger)}, expected {loggerClass}")

            if logargs:
                _logger.log(level, f"init: {self.__class__.__name__}({args=}, {kwargs=})", stacklevel=total_depth)
            else:
                _logger.log(level, f"init: {self.__class__.__name__}()", stacklevel=total_depth)

        if is_class:
            setattr(constructor, "__init__", init_wrapper)
            return constructor
        else:
            return init_wrapper

    return decorator


def on_call(logger: loggerClass, level=logging.DEBUG, logargs=True, depth=0):
    """
    When applied to a function, decorate it with a wrapper which logs the call using the given logger at the specified
    level.

    The "logger" argument must be an instance of a logger from the logging library.

    If logargs is True, log the function arguments, one per line.

    If the decorated function is to be nested inside other decorators, increase the depth argument by 1 for each
    additional level of nesting in order for the messages emitted to contain the correct source file name & line number.
    """
    const_depth = 2
    total_depth = const_depth + depth

    def decorator(func):

        if not callable(func):
            raise TypeError(f"{func} does not appear to be callable.")

        if not isinstance(logger, loggerClass):
            raise TypeError(f"logger argument had unexpected type {type(logger)}, expected {loggerClass}")

        if getattr(func, "__name__") == "__repr__":
            raise RuntimeError("Cannot apply to __repr__ as this will cause infinite recursion!")

        @wraps(func)
        def wrapper(*args, **kwargs):
            logger.log(level, f"calling {func} with {len(args)} arg(s) and {len(kwargs)} kwarg(s)", stacklevel=total_depth)
            if logargs:
                for n, arg in enumerate(args):
                    logger.log(level, f" - arg {n:>2}: {type(arg)} {arg}", stacklevel=total_depth)
                for m, (key, item) in enumerate(kwargs.items()):
                    logger.log(level, f" - kwarg {m:>2}: {type(item)} {key}={item}", stacklevel=total_depth)
            return func(*args, **kwargs)

        return wrapper

    return decorator
