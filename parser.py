#! /usr/bin/env python3.6
# -*- coding: utf-8 -*-

"""
Requires: sudo apt-get install expect python3
"""

from typing import Generator

from subprocess import Popen
from contextlib import contextmanager

import time
import os
import re

spaces = re.compile(r'\n+')


TMP_FILE = '/tmp/gaspaHomeSpeed'
SCRIPT_SH = os.getcwd() + '/' + 'script.sh'
MULTIPLIER = 2 ** 10 # Display KB/s


def write_file(down: float =0.0, up: float =0.0) -> None:
    """
    Write file with the last info.
    """
    with open(TMP_FILE, 'w') as f:
        f.write(str(int(round(time.time() * 1000))))
        f.write("\n")
        f.write(str(down))
        f.write("\n")
        f.write(str(up))


class SubshellException(Exception):
    pass


@contextmanager
def getIO(command: str) -> Generator[str, None, None]:
    """
    Run a command in its own process/shell.
    """
    with Popen(command, shell=True) as process:
        out, err = process.communicate()

    if err:
        raise SubshellException(f'Error while running process: {err}')

    if out:
        out = re.split(spaces, out)

    yield out


def main() -> None:
    with getIO(SCRIPT_SH) as out:
        result = str(out).split(":")

    import sys
    sys.exit(0)

    down = int((str(result[1]).split('('))[0]) / 1e6
    up = int((str(result[2]).split('('))[0]) / 1e6

    # Write data to our temporary file
    if os.path.exists(TMP_FILE):
        with open(TMP_FILE, 'r') as f:
            time_old = int(str(f.readline()))
            delta_time = (int(round(time.time() * 1e3)) - time_old) / 1e3
            old_down = float(f.readline())
            old_up = float(f.readline())

        write_file(down, up)

        # Down speed
        if old_down < down:
            print((down-old_down) / delta_time * MULTIPLIER)
        else:
            print(down / delta_time * MULTIPLIER)

        # Up speed
        if old_up < up:
            print((up - old_up) / delta_time * MULTIPLIER)
        else:
            print(up / delta_time * MULTIPLIER)
    else:
        write_file(down, up)


if __name__ == '__main__':
    main()