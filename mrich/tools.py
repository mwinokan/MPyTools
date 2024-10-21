
import re

def detect_format_prefix(message):

    match = re.match(f"^\[.*?\]", message)

    if match:
        match = match.group()

    return match

def strip_formats(*messages, text="", separator=" "):
    formats = []
    start = len(text) + 1
    for message in messages:

        if hasattr(message, "__rich__"):
            message = message.__rich__()
        else:
            message = str(message)

        prefix = detect_format_prefix(message)

        prefix_found = prefix is not None

        if prefix_found:
            message = message.removeprefix(prefix)
            prefix = prefix.removeprefix('[').removesuffix(']')

        end = start + len(message)
        text += separator + message
        
        if prefix_found:
            formats.append((prefix, start, end+2))
            
        start = end

    return text, formats
