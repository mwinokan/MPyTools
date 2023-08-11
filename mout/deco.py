
import time
from .output import debug, var
from .testing import TestStatus

def debug_log(func):

    def wrapper(*args, **kwargs):

        log_str = f'{func.__name__}('
        if args:
            try:
                arg_str = str(args).lstrip('(').rstrip(')')
            except AttributeError:
                arg_str = 'ARGS'

            log_str += arg_str
        if args and kwargs:
            log_str += ', '
        if args:
            log_str += str(kwargs).lstrip('{').rstrip('}')
        log_str += ')'
        debug(log_str)

        output = func(*args, **kwargs)

        if isinstance(output,TestStatus):
            if output.name is None:
                output.name = func.__name__
            output.print()
        else:
            var('result',f'{output}')

        print()

        return output
    
    return wrapper

def debug_time(func):

    def wrapper(*args, **kwargs):

        log_str = f'{func.__name__}('
        if args:
            log_str += str(args).lstrip('(').rstrip(')')
        if args and kwargs:
            log_str += ', '
        if args:
            log_str += str(kwargs).lstrip('{').rstrip('}')
        log_str += ')'
        debug(log_str)

        start = time.perf_counter()
        output = func(*args, **kwargs)
        end = time.perf_counter()

        if isinstance(output,TestStatus):
            if output.name is None:
                output.name = func.__name__
            output.print()
        else:
            var('result',f'{output}')
        
        var('time',f'{end-start}',unit='s')

        print()

        return output
    
    return wrapper
