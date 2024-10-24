from .console import console, console_print
from rich.text import Text
from .colors import COLOR_LOOKUP
from .tools import strip_formats

### STYLES


def bold(*messages, **kwargs):
    text, formats = strip_formats(*messages, **kwargs)
    text = Text(text)
    text.stylize("bold")
    for style, start, end in formats:
        text.stylize(style, start, end)
    return console_print(text)

def italic(*messages, **kwargs):
    text, formats = strip_formats(*messages, **kwargs)
    text = Text(text)
    text.stylize("italic")
    for style, start, end in formats:
        text.stylize(style, start, end)
    return console_print(text)

def underline(*messages, **kwargs):
    text, formats = strip_formats(*messages, **kwargs)
    text = Text(text)
    text.stylize("underline")
    for style, start, end in formats:
        text.stylize(style, start, end)
    return console_print(text)


### LOG

def warning(*messages, **kwargs):
    text = " Warning "
    text, formats = strip_formats(*messages, text=text, **kwargs)
    text = Text(f"{text}!")
    text.stylize("warning")
    text.stylize("reverse bold", 0, 9)
    for style, start, end in formats:
        text.stylize(style, start, end)
    return console_print(text)

def error(*messages, **kwargs):
    text = " ERROR "
    text, formats = strip_formats(*messages, text=text, **kwargs)
    text = Text(f"{text}!")
    text.stylize("error")
    text.stylize("reverse", 0, 7)
    for style, start, end in formats:
        text.stylize(style, start, end)
    return console_print(text)

def success(*messages, **kwargs):
    text = " Success "
    text, formats = strip_formats(*messages, text=text, **kwargs)
    text = Text(f"{text}!")
    text.stylize("success")
    text.stylize("reverse", 0, 9)
    for style, start, end in formats:
        text.stylize(style, start, end)
    return console_print(text)

def debug(*messages, **kwargs):
    text = "DEBUG:"
    text, formats = strip_formats(*messages, text=text, **kwargs)
    text = Text(f"{text}")
    text.stylize("debug")
    for style, start, end in formats:
        text.stylize(style, start, end)
    return console_print(text)

def title(*messages, **kwargs):
    text = ">>>"
    text, formats = strip_formats(*messages, text=text, **kwargs)
    text = Text(f"{text}")
    text.stylize("bold purple")
    for style, start, end in formats:
        text.stylize(style, start, end)
    return console_print(text)

def disk(message: str, *, prefix: str):
    message = str(message)
    text = Text(f" DISK  {prefix} {message}...")
    text.stylize("file", 0, 6)
    text.stylize("reverse bold", 0, 6)
    text.stylize("file", 8 + len(prefix), 8 + len(prefix) + len(message))
    return console_print(text)


def reading(message):
    return disk(message, prefix="Reading")


def writing(message):
    return disk(message, prefix="Writing")


def var(
    variable,
    value,
    unit: str | None = None,
    separator: str = "=",
    color: str | None = None,
    highlight: bool = True,
    highlight_if_rich_dunder: bool = False,
):

    variable = Text(str(variable), style=COLOR_LOOKUP["var_name"])
    variable.stylize("bold")

    if "Path" in str(type(value)):
        color = "file"

    if color and color in COLOR_LOOKUP:
        color = COLOR_LOOKUP[color]

    if hasattr(value, '__rich__'):
        highlight = highlight_if_rich_dunder
    
    if color:
        value = Text(str(value), style=color)

    objects = [variable, separator, value]

    if unit:
        unit = Text(unit, style=COLOR_LOOKUP["var_type"])
        objects.append(unit)

    console.print(*objects, markup=True, highlight=highlight)


### HEADINGS


def h1(message):
    from rich.panel import Panel

    text = Text(message.upper(), justify="center")
    text.stylize("bold")
    return console.print(Panel(text))


def h2(message):
    return console.rule(message)


def h3(message):
    from rich.panel import Panel

    return console.print(Panel.fit(message))


### ALIASES


def header(*args, **kwargs):
    return bold(*args, **kwargs)
