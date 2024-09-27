
from .console import console

# wrappers
def print(*args, **kwargs):
	console.print(*args, **kwargs)
def out(*args, **kwargs):
	console.out(*args, **kwargs)
def rule(*args, **kwargs):
	console.rule(*args, **kwargs)