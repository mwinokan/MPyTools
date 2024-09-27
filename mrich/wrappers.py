from .console import console


# wrappers
def print(*args, **kwargs):
    console.print(*args, **kwargs)


def out(*args, **kwargs):
    console.out(*args, **kwargs)


def rule(*args, **kwargs):
    console.rule(*args, **kwargs)


def track(*args, prefix: str = "Working...", **kwargs):
    from rich.progress import track

    return track(*args, description=prefix, **kwargs)
