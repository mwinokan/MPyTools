
from .console import console
from rich.text import Text

# log functions

def warning(message):	
	text = Text(f" Warning  {message}!")
	text.stylize("orange_red1")
	text.stylize("reverse bold", 0, 9)
	return console.print(text)

def error(message):	
	text = Text(f" ERROR  {message}!")
	text.stylize("bold bright_red")
	text.stylize("reverse", 0, 7)
	return console.print(text)

def success(message):	
	text = Text(f" Success  {message}!")
	text.stylize("bold bright_green")
	text.stylize("reverse", 0, 9)
	return console.print(text)

def debug(message):	
	text = Text(f"DEBUG: {message}")
	text.stylize("bright_black")
	return console.print(text)

def header(message):	
	text = Text(f"{message}")
	text.stylize("bold")
	return console.print(text)

def title(message):	
	text = Text(f">>> {message}")
	text.stylize("bold purple")
	return console.print(text)

def disk(message, prefix):	
	text = Text(f" DISK  {prefix} {message}...")
	text.stylize("bright_yellow reverse bold", 0, 6)
	text.stylize("bright_yellow", 8+len(prefix), 8+len(prefix)+len(message))
	return console.print(text)

def reading(message):
	return disk(message, 'Reading')

def writing(message):
	return disk(message, 'Writing')

def var(variable, value, unit=None, separator="=", colour='magenta'):	
	value = str(value)
	if unit:
		unit = str(unit)
		text = Text(f"{variable} {separator} {value} {unit}")
		text.stylize("steel_blue1", 0, len(variable))
		text.stylize("steel_blue1", len(variable)+len(separator)+2+len(value), len(variable)+len(separator)+3+len(value)+len(unit))
	else:
		text = Text(f"{variable} {separator} {value}")
		text.stylize("steel_blue1", 0, len(variable))
	
	# text.stylize("bright_yellow", 8+len(prefix), 8+len(prefix)+len(message))
	return console.print(text)
