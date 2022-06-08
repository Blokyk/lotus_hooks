from utils import *
from artifacts import generate_artifacts, generate_error_artifacts, link_artifacts

def build_test(commit: str, options: GitOptions) -> bool:
    print(" • Building... ")

    build_output = run([dotnet, "build", "-c", "Release", "-noLogo", "-clp:noSummary", "-clp:ForceConsoleColor"])

    if (build_output.retcode != 0):
        print("\t",fmt_failed())
        print("\tThere were [red]errors[/] while building commit", fmt_commit(commit))
        write(indent('\n'.join(build_output.output.splitlines())[3:], 2))
        print("\t[italic red]Fix theses errors before committing")
        return False

    print("\t",fmt_ok())
    return True

def generic_test(commit: str, options: GitOptions) -> bool:
    print(" • Options... ")

    print("\tHelp... ")

    help_output = parsex("help")

    if (help_output.retcode > 1):
        print("\t\t",fmt_failed())
        print("\t\t[bold][red]Error running the 'help' option :")
        write(indent(help_output.output, 3))
        return False

    print("\t\t",fmt_ok())

    print("\tSilent... ")

    silent_output = parsex("silent")

    if (silent_output.retcode != 0):
        print("\t\t",fmt_failed())
        print("\t\t[bold][red]Error running the 'silent' option :")
        write(indent(silent_output.output, 3))
        return False

    print("\t\t",fmt_ok())

    print("\tPrint... ")

    print_output = parsex("print")

    if (print_output.retcode != 0):
        print("\t\t",fmt_failed())
        print("\t\t[bold][red]Error running the 'print' option :")
        write(indent(print_output.output, 3))
        return False

    print("\t\t",fmt_ok())

    print("\tGraph/hash... ")

    graph_output = parsex("graph")

    if (graph_output.retcode != 0):
        print("\t\t",fmt_failed())
        print("\t\t[bold][red]Error running the 'graph' option :")
        write(indent(graph_output.output, 3))
        return False

    print("\t\t",fmt_ok())

    print("\tConstant graph/hash... ")

    constant_graph_output = parsex("graph")

    if (constant_graph_output.retcode != 0):
        print("\t\t",fmt_failed())
        print("\t\t[bold][red]Error running the 'graph constant' option :")
        write(indent(constant_graph_output.output, 3))
        return False

    print("\t\t",fmt_ok())

    return True

def hash_test(
    commit: str,
    bypass_hash: bool,
    hash_file: Path,
    options: GitOptions
) -> bool:
    print(" • Hash... ")

    hash_output = parsex("hash").output

    runtime_hash = hash_output
    expected_hash = ""

    if (bypass_hash):
        new_hash = options["bypass_hash"]

        if new_hash == None:
            hash_file.write_text(runtime_hash)
        else:
            hash_file.write_text(options["bypass_hash"])

        print("\t",fmt_warn("OVERRIDDEN"))

    expected_hash = hash_file.read_text().splitlines()[0] # remove ending newline

    if (runtime_hash != expected_hash):
        print("\t",fmt_failed("MISMATCH"))
        print(f"\tExpected [bold cyan]{expected_hash}[/], but instead got [bold yellow]{runtime_hash}[/]")
        return False

    print("\t",fmt_ok())

    return True

def graph_test(commit: str, prev_ref: str, bypass_visual: bool, no_visual: bool, hash_file: Path, artifact_dir: Path, tmpdir: Path, options: GitOptions) -> bool:
    print(" • Graph... ")

    if no_visual:
        print("\t",fmt_failed("REJECTED"))
        print("\t[red]Option '[bold]no_visual[/]' specified. Since hash check failed, rejecting.")
        #TODO: cleanup
        return False

    if bypass_visual:
        print("\t",fmt_warn("BYPASSED"))
        print("\t[yellow]Option '[bold]bypass_visual[/]' specified, so accepting despite hash mismatch")
        #TODO: cleanup
        return True

    #if ("no_visual" in options):
    #    print("[italic]no_visual[/] was specified, rejecting directly")
    #    print("If this was intended, resubmit this push with [italic green]--push-option='hash_" + commit + "=" + graph_hash + "'[/].")
    #    exit(1)

    print()
    print("\tChecking for visual differences... ", end="")

    graph_output = parsex("graph").output

    new_path = join(artifact_dir, commit + ".dot")
    prev_path = join(artifact_dir, prev_ref + ".dot")

    with open(new_path, "w+") as f:
        f.write(graph_output)

    if (dot_result := run(["dot", "-Tpng", "-O", new_path])).retcode != 0:
        print("\t",fmt_failed())
        print("\t[bold red]Could not generate new png :")
        write(indent(dot_result.output, 2))
        return False

    if (diff_result := run(["diff", prev_path + ".png", new_path + ".png"])).retcode != 0:
        # If it's one, then the graphs are different
        if (diff_result.retcode != 1):
            print("\t",fmt_failed())
            print("\t[bold red]An error occurred while trying to diff graphs pictures :")
            write(indent(diff_result.output, 2))
            return False

        print("\t",fmt_failed("DIFFERENT"))

        error("Graphs visually differed !")
        error("[not bold]Expected [yellow]"
            + run(["sha1sum", "-b", prev_path + ".png"]).output[0:7]
            + "[/], got [yellow]"
            + run(["sha1sum", "-b", new_path + ".png"]).output[0:7]
        )

        generate_error_artifacts(new_path, prev_path, abspath("compare.png"))
        return False
    print("\t",fmt_ok())

    generate_artifacts(new_path, prev_path)
    print("Putting hash", graph_output.splitlines()[-1][2:], "back into the file")
    hash_file.write_text(graph_output.splitlines()[-1][2:])
    link_artifacts(new_path, prev_path)
    return True
