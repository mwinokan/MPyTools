from IPython import get_ipython

d = get_ipython()

if d and "IPKernelApp" in d.config:  # Checks for Jupyter kernel

    from rich.jupyter import JUPYTER_HTML_FORMAT

    if "margin:0px" not in JUPYTER_HTML_FORMAT:
        print(
            "mrich: Jupyter may show unwanted line-spacing, run `mrich.patch_rich_jupyter_margins()` to patch"
        )


def patch_rich_jupyter_margins():

    from rich.jupyter import JUPYTER_HTML_FORMAT

    if "margin:0px" in JUPYTER_HTML_FORMAT:
        print("mrich: rich.jupyter already patched")
        return

    from rich import jupyter

    RICH_JUPYTER_PATH = jupyter.__file__

    # Define the strings to search and replace
    target_string = """<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace">{code}</pre>"""
    replacement_string = """<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace;margin:0px">{code}</pre>"""

    # Step 1: Read the file content
    with open(RICH_JUPYTER_PATH, "r") as file:
        file_contents = file.read()

    # Step 2: Replace the target string with the replacement string
    updated_contents = file_contents.replace(target_string, replacement_string)

    # Step 3: Write the modified content back to the file
    with open(RICH_JUPYTER_PATH, "w") as file:
        file.write(updated_contents)

    print("mrich: patched rich.jupyter HTML margins")
