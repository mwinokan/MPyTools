from rich.console import Console
from .colors import THEME

console = Console(theme=THEME)

from rich.traceback import install

install(show_locals=True)
