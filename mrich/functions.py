from .console import console
from rich.text import Text
from .colors import COLOR_LOOKUP

### LOG


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


def title(message):
    text = Text(f">>> {message}")
    text.stylize("bold purple")
    return console.print(text)


def disk(message: str, prefix: str):
    message = str(message)
    text = Text(f" DISK  {prefix} {message}...")
    text.stylize("bright_yellow reverse bold", 0, 6)
    text.stylize("bright_yellow", 8 + len(prefix), 8 + len(prefix) + len(message))
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
