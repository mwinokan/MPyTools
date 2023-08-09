
from .output import warning, error, out, var

import mcol

class TestStatus:

    total_warnings = 0
    total_errors = 0

    def __init__(self,name=None):
        
        self.name = name
        self.warnings = []
        self.errors = []

    @property
    def num_warnings(self):
        return len(self.warnings)

    @property
    def num_errors(self):
        return len(self.errors)

    def warning(self,message):
        warning(message)
        self.increment_total_warnings()
        self.warnings.append(message)

    def error(self,message):
        error(message)
        self.increment_total_errors()
        self.errors.append(message)
    
    @property
    def passed(self):
        return self.num_errors == 0
    
    def print(self):
        out(f'{mcol.func}{self.name}{mcol.clear}: {mcol.warning if self.num_warnings else mcol.success}{self.num_warnings}{mcol.clear} Warnings, {mcol.error if self.num_warnings else mcol.success}{self.num_errors}{mcol.clear} Errors,  Passed={mcol.success if self.passed else mcol.error}{self.passed}{mcol.clear}')

    @classmethod
    def summary(cls):
        if cls.total_warnings:
            warning(f'{cls.total_warnings} warnings')

        if cls.total_errors:
            error(f'{cls.total_errors} errors')

    @classmethod
    def increment_total_warnings(cls):
        cls.total_warnings += 1

    @classmethod
    def increment_total_errors(cls):
        cls.total_errors += 1
