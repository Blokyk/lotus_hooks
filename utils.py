#!/bin/env python3

import re
import sys

from os.path import abspath, exists, isfile, join, basename
from pathlib import Path
from typing import Dict, Iterable, Set

from log_utils  import *
from cmd_utils  import *
from git_utils  import *
from opt_utils  import *
from misc_utils import *


dotnet = "/usr/bin/dotnet"
#dotnet = "/home/ubuntu/.dotnet/dotnet"