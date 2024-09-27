from rich.console import Console

console = Console()

from rich.traceback import install

install(show_locals=True)
