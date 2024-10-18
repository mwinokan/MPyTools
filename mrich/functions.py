from .console import console
from rich.text import Text
from .colors import COLOR_LOOKUP
from .tools import detect_format_prefix, strip_formats

### LOG

def warning(message):
    text = Text(f" Warning  {message}!")
    text.stylize("warning")
    text.stylize("reverse bold", 0, 9)
    return console.print(text)


def error(message):
    text = Text(f" ERROR  {message}!")
    text.stylize("error")
    text.stylize("reverse", 0, 7)
    return console.print(text)


def success(*messages, **kwargs):
    text = " Success "
    text, formats = strip_formats(*messages, text=text, **kwargs)
    text = Text(f"{text}!")
    text.stylize("success")
    text.stylize("reverse", 0, 9)
    # text.stylize("on bright_white", 0, 9)
    for style, start, end in formats:
        text.stylize(style, start, end)
    return console.print(text)

def debug(message):
    text = Text(f"DEBUG: {message}")
    text.stylize("debug")
    return console.print(text)


def title(message):
    text = Text(f">>> {message}")
    text.stylize("bold purple")
    return console.print(text)


def disk(message: str, *, prefix: str):
    message = str(message)
    text = Text(f" DISK  {prefix} {message}...")
    text.stylize("file", 0, 6)
    text.stylize("reverse bold", 0, 6)
    text.stylize("file", 8 + len(prefix), 8 + len(prefix) + len(message))
    return console.print(text)


def reading(message):
    return disk(message, "Reading")


def writing(message):
    return disk(message, "Writing")


def var(
    variable,
    value,
    unit: str | None = None,
    separator: str = "=",
    color: str | None = None,
    highlight: bool = True,
    highlight_if_rich_dunder: bool = False,
):

    variable = Text(variable, style=COLOR_LOOKUP["var_name"])
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


### STYLES


def bold(message):
    text = Text(message)
    text.stylize("bold")
    return console.print(text)


def italic(message):
    text = Text(message)
    text.stylize("italic")
    return console.print(text)


def underline(message):
    text = Text(message)
    text.stylize("underline")
    return console.print(text)


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
