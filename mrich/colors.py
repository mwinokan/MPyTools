
COLOR_LOOKUP = {
	"var_name": "cyan",
	"var_type": "hot_pink",
	"file": "gold3",
	"result": "cornflower_blue",
	"success": "bold green",
	"error": "bold red",
	"warning": "dark_orange",
	"arg": "cyan3",
	"debug": "bright_black",
}

from rich.theme import Theme
THEME = Theme(COLOR_LOOKUP, inherit=True)
