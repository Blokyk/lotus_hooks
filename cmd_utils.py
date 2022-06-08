from sys import stdin as STDIN
from subprocess import CalledProcessError, check_output, STDOUT as stdout_id
from os import environ as env, chdir as os_chdir, strerror

from typing import Any, List, NamedTuple, NoReturn, Union

class CmdResults(NamedTuple):
    retcode: int
    output: str

parsex_path: str = ""

def run(args: Union[List[str], str]) -> CmdResults:
    if type(args) is str:
        args = args.split()
    output = ""
    retcode = 0
    try:
        output = check_output(args, stderr=stdout_id)
    except CalledProcessError as e:
        output = e.output
        retcode = e.returncode
    return CmdResults(retcode, output.decode("utf-8")[:-1])

def parsex(args: Union[List[str], str]) -> CmdResults:
    assert parsex_path != ""

    if args is List[str]:
        return run([parsex_path] + list(args))
    else:
        return run([parsex_path, str(args)])

def chdir(path: str) -> None:
    os_chdir(path)
    env["PWD"] = path

def split_stdin(separator: str = " ") -> List[str]:
    return STDIN.readline().split(separator)

