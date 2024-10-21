from .console import console

# wrappers
def print(*args, **kwargs):
    console.print(*args, **kwargs)


def out(*args, **kwargs):
    console.out(*args, **kwargs)


def rule(*args, **kwargs):
    console.rule(*args, **kwargs)

### PROGRESS

CURRENT_PROGRESS = None

def clear_progress():
    global CURRENT_PROGRESS
    CURRENT_PROGRESS = None

def track(*args, prefix: str = "Working...", **kwargs):
    
    from .colors import THEME
    from rich.console import Console
    from rich.progress import Progress, TextColumn, BarColumn, TaskProgressColumn, TimeRemainingColumn, TimeElapsedColumn

    global CURRENT_PROGRESS

    console = Console(theme=THEME)

    CURRENT_PROGRESS = Progress(
        *Progress.get_default_columns(),
        console=console,
    )

    with CURRENT_PROGRESS:
        yield from CURRENT_PROGRESS.track(
            *args, description=prefix, **kwargs
        )
    