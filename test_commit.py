#!/bin/env python3

import sys

from utils import *

from tests import build_test, graph_test, hash_test, generic_test

import cmd_utils

OLD_QUATANTINE_PATH: str

repo_dir=Path()
branch_name: str
artifact_dir=Path()

def init(repo_dir: str, branch_name: str, artifact_dir: str):
    globals()["branch_name"] = branch_name
    globals()["repo_dir"] = Path(abspath(repo_dir))
    globals()["artifact_dir"] = Path(abspath(artifact_dir))

def cleanup(tmpdir: Path = None) -> None:  # type: ignore
    if (globals()["OLD_GIT_QUARANTINE_PATH"] != None):
            env["GIT_QUARANTINE_PATH"]=globals()["OLD_GIT_QUARANTINE_PATH"]

    env["GIT_DIR"]="." # gitdir is current dir for bare repos

    chdir(str(repo_dir))

    # if tmpdir is assigned
    if (tmpdir != None):
        rm_result = run(["rm", "-Rf", str(tmpdir)])
        if (rm_result.retcode != 0):
            print(
                "[bold red]WTF is happening. Trying to remove the temp directory returned code",
                rm_result.retcode,
                "and output \"",
                rm_result.output,
                "\""
            )

def test_commit(commit: str, options: GitOptions) -> CmdResults:

    globals()["OLD_GIT_QUARANTINE_PATH"]=env.get("GIT_QUARANTINE_PATH")

    if (globals()["OLD_GIT_QUARANTINE_PATH"] != None):
        del env["GIT_QUARANTINE_PATH"]

    #artifact_dir = artifact_dir
    #branch_name = branch_name
    repo = repo_dir

    commit = rev_parse(commit, True)

    prev_ref = rev_parse(commit+"~1")

    hash_file = artifact_dir.joinpath("hash-" + branch_name)

    if not (isfile(hash_file)):
        cleanup()
        return CmdResults(2, f"[bold][yellow]{hash_file}[red] is not a valid file")

    hash_file = Path(abspath(hash_file))

    tmpdir = artifact_dir.joinpath("parsex-clone")

    run(["mkdir", str(tmpdir)])

    clone_result = run(["git", "clone", str(repo), str(tmpdir)])

    if (clone_result.retcode != 0):
        cleanup(tmpdir)
        return CmdResults(3, "[bold red]Failed to clone repo : [/]\n[italic]" + indent(clone_result.output))

    chdir(str(tmpdir))
    env["GIT_DIR"]=join(".git")

    print()
    print(Panel.fit(" ".join(["[bold white]Testing commit", fmt_commit(commit), "[bold white]against", fmt_commit(prev_ref)])))
    print()

    checkout_result = run(["git", "checkout", commit])

    print(rev_parse("HEAD"))

    if (checkout_result.retcode != 0 or rev_parse("HEAD") != commit):
        cleanup(tmpdir)
        return CmdResults(
            4,
            "[bold red]Failed to checkout [/]"
          + fmt_commit(commit)
          + "[bold red] : [/]\n[italic]"
          + indent(checkout_result.output)
        )

    diff_option = 1 if "show_diff" in options else 2 if "show_long_diff" in options else 0

    if (diff_option != 0):
        print("Diff from", fmt_commit(prev_ref), "to", fmt_commit(commit), ": ")
        print(run(["git", "diff", "color=always", "--stat" if diff_option == 2 else "--shortstat", prev_ref, commit]).output)

    print("Running tests :")

    print()

    if not build_test(commit, options):
        cleanup(tmpdir)
        return CmdResults(1, "[bold red]Build failed")

    cmd_utils.parsex_path = tmpdir.joinpath("bin/Release/net6/parsex")

    print()

    if not generic_test(commit, options):
        cleanup(tmpdir)
        return CmdResults(1, "[bold red]Error compiling test.txt")

    print()

    bypass_all = "bypass_all" in options
    bypass_hash = bypass_all or ("bypass_hash" in options)
    bypass_visual = bypass_all or ("bypass_visual" in options)

    if not hash_test(commit, bypass_hash, hash_file, options):
        if not graph_test(commit, prev_ref, bypass_visual, "no_visual" in options, hash_file, artifact_dir, tmpdir, options):
            cleanup(tmpdir)
            return CmdResults(1, "Neither the hash nor the graph matched... ")

    cleanup(tmpdir)
    return CmdResults(0, "")

