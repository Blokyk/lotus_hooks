import sys
from log_utils import print

from rich import box
from rich.panel import Panel


def is_number(s: str) -> bool:
    if len(s) > 0 and s[0] in ('-', '+'):
        return s[1:].isdigit()
    return s.isdigit()


def display_help():
    print(Panel.fit("""Appending an underscore and a commit hash to any of
those option names will only apply it to that
commit (although it could affect those after it, like in
the case of [italic bold]hash_<commit>[/], where the
updated hash will be used for subsequent commits)""", title="[bold]Note"), justify="center")

    print()

    print("[bold italic green]-- Display --", justify="center")
    print()
    print("[bold]show_diff", justify="center")
    print("Shows a short summary of the changes in each commit", justify="center")
    print()
    print("[bold]show_long_diff", justify="center")
    print("Shows a complete diff of the changes in each commit", justify="center")

    print()
    print

    print("[bold italic green]-- Testing --", justify="center")
    print()
    print("[bold]bypass_hash[italic not bold][=<new-hash>][/]", justify="center")
    print(
"""When testing commits, bypass checks for the graph hash.
If no new hash is specified, it will automatically be
determined at each commit""", justify="center")
    print()
    print("[bold]bypass_visual", justify="center")
    print("In case of a hash mismatch, bypass visual checks and update", justify="center")
    print()
    print("[bold]bypass_all", justify="center")
    print("Equivalent to bypass_hash + bypass_visual", justify="center")
    print()
    print("[bold]no_visual", justify="center")
    print(
"""If there's a hash mismatch, directly reject without
checking for visual equivalence. This is basically the
opposite of [bold]bypass_visual[/] since it automatically [italic]rejects[/]
the commit instead of accepting it blindly.""", justify="center")

    print()
    print()

    print("[bold italic green]-- Pushing behavior --", justify="center")
    print()
    print("[bold]publish", justify="center")
    print("Once validated, forwards the current push to the origin", justify="center")
    print()
    print("[bold]test, dry", justify="center")
    print("Validate the commits, but don't accept them", justify="center")

    print()
    print()

    print("[dim]This push won't do anything, don't worry about it being 'rejected'", justify="center")
