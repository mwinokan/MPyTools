from rich.console import Console
from .colors import THEME

console = Console(theme=THEME)

from rich.traceback import install

install(show_locals=True)

def console_print(*args, **kwargs):

	from .wrappers import CURRENT_PROGRESS, clear_progress

	if CURRENT_PROGRESS is not None:
		if CURRENT_PROGRESS.finished:
			clear_progress()
			return console.print(*args, **kwargs)
		else:
			return CURRENT_PROGRESS.console.print(*args, **kwargs)

	return console.print(*args, **kwargs)
