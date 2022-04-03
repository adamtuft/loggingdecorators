# loggingdecorators

Simple, easy-to-use decorators for logging object initialisation and function calls using the
core `logging` module.

This package provides 2 decorators which allow you to separate logging functionality
from business logic.

Note that these decorators perform no logging setup, this is left to the user.

## on_init

```python
on_init(
    logger: typing.Union[str, logging.Logger]="logger",
    level=logging.DEBUG,
    logargs=True,
    depth=0
)
```

When applied to a class or an `__init__` method, decorate it with a wrapper which logs the `__init__` call using the
given logger at the specified level.

If `logger` is a string, look up an attribute of this name in the initialised object and use it to log the message.
Otherwise, assume `logger` is an instance of a logger from the logging library and use it to log the message.

If `logargs` is `True`, the message contains the arguments passed to `__init__`.

If the decorated class or `__init__` method is to be nested inside other decorators, increase the depth argument by 1
for each additional level of nesting in order for the messages emitted to contain the correct source file name &
line number.

### Examples

1. Applied directly to a user-defined class:

```python
from loggingdecorators import on_init
from logging import getLogger


# as a class decorator...
@on_init(logger=getLogger())
class Widget:
    ...


class OtherWidget:

    # ... or as an __init__ decorator
    @on_init(logger=getLogger())
    def __init__(self):
        ...
```

2. Decorating a built-in class using a subclass:

```python
from loggingdecorators import on_init
from collections import defaultdict
from logging import getLogger


@on_init(logger=getLogger())
class defaultdict_log(defaultdict):
    pass
```

**Note:** it is not recommended to directly decorate a built-in class unless you want
all initialisations of that class to be logged, as this decorator replaces the class'
`__init__` method.

3. Decorating a class in a subclass with a mixin:

```python
from loggingdecorators import on_init
from logging import getLogger


class Widget:
    ...


class LoggingMixin:

    @on_init(logger=getLogger())
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        
class LoggingWidget(LoggingMixin, Widget):
    pass
```

## on_call

```python
on_call(
    logger: logging.Logger,
    level=logging.DEBUG,
    logargs=True,
    depth=0
)
```

When applied to a function, decorate it with a wrapper which logs the call using the given logger at the specified
level.

The `logger` argument must be an instance of a logger from the logging library.

If `logargs` is `True`, log the function arguments, one per line.

If the decorated function is to be nested inside other decorators, increase the `depth` argument by 1 for each
additional level of nesting in order for the messages emitted to contain the correct source file name & line number.

### Examples

1. Directly decorating a function:

```python
from loggingdecorators import on_call
from logging import getLogger

@on_call(logger=getLogger())
def interesting_function(*args, **kwargs):
    ...

interesting_function()
```

2. Creating a logging version of another function:

```python
from loggingdecorators import on_call
from logging import getLogger

def interesting_function(*args, **kwargs):
    ...

decorator = on_call(logger=getLogger())
interesting_function_log = decorator(interesting_function)

interesting_function_log()
```
