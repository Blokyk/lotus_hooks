#!/bin/env python3

from sys import exit

from click import option

from utils import *

from test_commit import init, test_commit

options = parse_options()

dev_dir = "/home/blokyk/docs/dev/git_hooks/parsex_hooks"

if "help" in options:
    display_help()
    sys.exit(1)

if "bypass_all" in options:
    del options["bypass_all"]
    options.add_option("bypass_hash")
    options.add_option("bypass_visual")

# Backup the current

if (bundle_result := run(f"git bundle create {dev_dir}/../.artifacts/.backup/parsex/parsex_" + run("date +'%H-%M-%S_%y-%m-%d'").output +" --all")).retcode != 0:
    dim_warn(f"Could not create repo backup (retcode = {bundle_result.retcode})")
    dim(bundle_result.output)

print()

### Parse and check commits and branches ###
a = [old_ref, new_ref, branch] = split_stdin(" ")

branch = basename(branch[:-1])

new_ref = rev_parse(new_ref)

# See section on pre-receive in `man githooks`
#
# Basically, git sets old_ref to "the null object" when pushing to a new branch
if old_ref[:7] == "0000000" or not ref_exists(branch):
    old_ref=rev_parse(run(f"git merge-base HEAD {new_ref}").output)
    print("This seems like a new branch, basing it on last known ancestor", fmt_commit(old_ref))

commit_list = []

# Checks the commit after old_ref. If it's the same as new_ref, then we're only pushing a single commit
if ((next_ref := next_commit(old_ref, new_ref)) == new_ref):
    print("Pushing", fmt_commit(new_ref), "on branch", fmt_branch(branch))
    commit_list = [new_ref]
else:
    print("Pushing from", fmt_commit(next_ref), "to", fmt_commit(new_ref), "on branch", fmt_branch(branch))

    commit_list = run("git rev-list --abbrev-commit " + old_ref + ".." + new_ref).output.splitlines()

    commit_list.reverse()

    print("There's [bold cyan]" + str(len(commit_list)) + "[/] commits to test", end=" ")

    if (len(options.get_global_options()) != 0):
        print("(w/", ", ".join((opt if val == None else opt + "=" + str(val)) for opt, val in options.get_global_options()) + ")", end=" ")
    print(":")

    for commit in commit_list:
        if (len(options.get_options_for_commit(commit)) != 0):
            #if ("bypass_all" in options.get_options_for_commit(commit) or
            #    "bypass_hash" in options.get_options_for_commit(commit) or
            #    "bypass_visual" in options.get_options_for_commit(commit)):
            print("\t-", fmt_commit(commit), "(w/", ", ".join((opt if val == None else opt + "=" + str(val)) for opt, val in options.get_options_for_commit(commit)) + ")")
        else:
            print("\t-", fmt_commit(commit))

init("./", branch, f"{dev_dir}/../.artifacts/")

for commit in commit_list:
    # TODO: We have to add global options but overwrite those specified in the per-commit options
    opts = options.get_global_options()

    for (opt, val) in options.get_options_for_commit(commit):
        opts[opt] = val

    test_result = test_commit(commit, GitOptions(opts))

    if (test_result.retcode != 0):
        print("[bold red]Commit", fmt_commit(commit), "[bold red]isn't valid")

        if test_result.retcode == 1:
            sys.exit(1)

        print("[bold red]Failed with retcode", test_result.retcode, "[bold red]and output :")
        print(test_result.output)
        sys.exit(test_result.retcode)

    print("[bold white]Congrats! Commit", fmt_commit(commit), "[bold white]is valid!")
