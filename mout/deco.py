
from .output import debug, var
from .testing import TestStatus

def debug_log(func):

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
