# no shebang-line as Python scripts aren't really executable on Windows
# use runner = ["python", "runner.py"] in your Cargo config instead

from hashlib import sha3_224
from shlex import quote
import os
import pathlib
import platform
import sys
import subprocess as sp

# "parse" command line
EXECUTABLE = sys.argv[1]
ARGUMENTS = sys.argv[2:]

# get relative part of executable path and convert to POSIX (as host may be Windows)
EXECUTABLE_RELATIVE = pathlib.Path(os.path.relpath(EXECUTABLE)).as_posix()

# create a (statistically) unique name for the remote working directory copy
WORKDIR = sha3_224((platform.node() + ':' + os.getcwd()).encode('utf-8')).hexdigest()

# the target hardware (Bela.io) has passwordless root login
# for normal systems you'll need to handle user authentication in a smarter manner
SSH_NONINTERACTIVE = ['ssh', '-qTo', 'BatchMode yes', 'root@bela.local']
SSH_INTERACTIVE = ['ssh', '-qt', 'root@bela.local']

# use rsync via WSL when on Windows
RSYNC = (['wsl'] if platform.system() == 'Windows' else []) + ['rsync']

# ensure base directory exists
sp.run(SSH_NONINTERACTIVE + [
    'mkdir', '-p', '.cargo_runner'
], stdout=sp.DEVNULL, stderr=sp.DEVNULL, check=True)

# synchronize working directory to remote
sp.run(RSYNC + [
    '-rlptz',
    # prevent syncing the .git folder
    '--exclude', '.git',
    # the following files can be very large and are usually not required on the Bela
    '--exclude', '*.d',
    '--exclude', '*.rlib',
    '--exclude', '*.rmeta',
    '--exclude', '*.exe',
    '--exclude', '*.exp',
    '--exclude', '*.lib',
    '--exclude', '*.pdb',
    # delete old files (otherwise they'll get copied back later)
    '--delete',
    '.',
    f'root@bela.local:.cargo_runner/{WORKDIR}/'
], stdout=sp.DEVNULL, stderr=sp.DEVNULL, check=True)

# run executable remotely, explicitly without checking, as partial results should still be copied
code = sp.run(SSH_INTERACTIVE + [
    f'cd .cargo_runner/{WORKDIR} && {quote(EXECUTABLE_RELATIVE)} {" ".join(map(quote, ARGUMENTS))}'
]).returncode

# synchronize working directory from remote (for Criterion reports etc.)
sp.run(RSYNC + [
    '-rlptz',
    f'root@bela.local:.cargo_runner/{WORKDIR}/',
    '.',
], stdout=sp.DEVNULL, stderr=sp.DEVNULL, check=True)

# exit with the code from the actual run
sys.exit(code)
