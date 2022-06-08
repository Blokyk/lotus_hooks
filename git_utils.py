
from cmd_utils import CmdResults, run

def rev_parse(ref: str, short: bool = True) -> str:
    return result.output if (result := try_rev_parse(ref, short)).retcode == 0 else ""
def try_rev_parse(ref: str, short: bool = True) -> CmdResults:
    return run(["git", "rev-parse", ("--short" if short else ""), ref])


def ref_exists(refname: str) -> bool:
    return run(f"git rev-parse --verify {refname}").retcode == 0

def next_commit(ref: str, branch: str) -> str:
    return run(f"git rev-list --abbrev-commit --reverse {ref}..{branch}").output.splitlines()[0]
