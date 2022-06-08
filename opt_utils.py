from git_utils import rev_parse, try_rev_parse
from log_utils import dim_warn
from misc_utils import is_number

import re
from os import environ as env
from typing import Any, Dict

class GitOptions:
    __options: Dict[str, Any]
    __commit_opt: Dict[str, Dict[str, Any]]

    def __init__(self, options: Dict[str, Any]):
        self.__options = options
        self.__commit_opt = {}

    def __len__(self) -> int:
        return self.get_option_count()

    def __iter__(self):
        return iter(self.__options)

    def __contains__(self, item: str) -> bool:
        if ("*" not in item):
            return item in self.__options

        for key in self.__options.keys():
            if re.search(item, key):
                return True
        return False

    def __setitem__(self, key: str, value: Any):
        self.add_param(key, value)

    def __getitem__(self, key: str) -> Any:
        return self.__options[key]

    def __delitem__(self, key: str) -> None:
        del self.__options[key]

    def get_option_count(self) -> int:
        return len(self.__options)

    def add_option(self, name: str):
        self.add_param(name, None)

    def add_param(self, name: str, value: Any):
        if name in self.__options:
            dim_warn("Found duplicated option [not dim][white]" + name)

        self.__options[name] = value

    def get_global_options(self) -> Dict[str, Any]:
        output = {}

        for (k, v) in self.__options.items():
            possible_commit = k.split("_")[-1]

            possible_short = try_rev_parse(possible_commit)

            if possible_short.retcode != 0:
                output[k] = v

        return output

    def get_options_for_commit(self, commit: str) -> Dict[str, Any]:
        if (commit in self.__commit_opt):
            return self.__commit_opt[commit]

        self.__commit_opt[commit] = {}

        commit_copy = rev_parse(commit)

        for (k, v) in self.__options.items():
            possible_commit = k.split("_")[-1]

            possible_short = try_rev_parse(possible_commit)

            if possible_short.retcode == 0 and possible_short.output == commit_copy:
                self.__commit_opt[commit][k.replace("_" + possible_commit, "")] = v


        return self.__commit_opt[commit]

def parse_options() -> GitOptions:
    option_count = int(env.get("GIT_PUSH_OPTION_COUNT", 0))
    options = GitOptions({})
    for i in range(0, option_count):
        temp = env["GIT_PUSH_OPTION_"+str(i)]
        if ("=" in temp):
            split_temp = temp.split("=", maxsplit=1)

            k = split_temp[0]
            v = split_temp[-1]

            if is_number(v):
                v = int(v)
            elif v.lower() in ["t", "true"]:
                v = True
            elif v.lower() in ["f", "false"]:
                v = False
            options.add_param(k, v)
        else:
            options.add_option(temp)

    return options
