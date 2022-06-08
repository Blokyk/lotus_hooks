
from typing import Any

from rich.style import Style
from rich.console import Console
from rich.traceback import install

install(show_locals=True)

stdout = Console(color_system="truecolor", width=72)

print = stdout.print
status = stdout.status
write = stdout.out

def dim(*msg: Any, italic: bool = True):
    """Print $objects with [dim italic]"""
    print(msg, style=Style(dim=True, italic=italic))

def dim_warn(*msg: Any, italic: bool = True):
    """Print $objects with [dim italic yellow]"""
    print(msg, style=Style(color="yellow", dim=True, italic=italic))
def warn(*msg: Any, italic: bool = True):
    """Print $objects with [italic yellow]"""
    print(msg, style=Style(color="yellow", italic=italic))

def error(*msg: Any, italic: bool = True):
    """Print $msg with [italic red]"""
    print(msg, style=Style(color="red", bold=True, italic=italic))

def fmt_commit(ref: str) -> str:
    """Return markup for printing commits"""
    return "[bold green]" + ref + "[/]"

def fmt_branch(branch: str):
    """Return markup for printing branch names"""
    return "[bold white]" + branch + "[/]"

def indent(text: str, n: int = 1):
    return (n*'\t') + text.replace('\n', '\n' + n*'\t')

def fmt_failed(status: str = "FAILED"):
    return "[bold]" + status + " [red]✘[/][/]"
def fmt_warn(status: str = "WARNING"):
    return "[bold]" + status + " [yellow]Δ[/][/]"
def fmt_ok(status: str = "OK"):
    return "[bold]" + status + " [green]✔[/][/]"