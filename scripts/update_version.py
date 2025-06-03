
import os, pathlib
import datetime


# v  = '0.4.35'  # 2025-05-13
version_str  = '0.4.50'







dirREPO      = pathlib.Path( __file__ ).parent.parent
date_str     = str( datetime.date.today() )



# update __init__.py
fpathINIT = os.path.join(dirREPO, 'spm1d', '__init__.py')
with open(fpathINIT, 'r') as f:
    lines = f.readlines()
    for i,line in enumerate(lines):
        if line.startswith('__version__'):
            break
    lines[i] = f"__version__ = '{version_str}'  # {date_str}\n"
with open(fpathINIT, 'w') as f:
    f.writelines( lines )



# update setup.py
fpath = os.path.join(dirREPO, 'setup.py')
with open(fpath, 'r') as f:
    lines = f.readlines()
    for i,line in enumerate(lines):
        if line.startswith('    version'):
            break
    lines[i] = f"    version          = '{version_str}',\n"
with open(fpath, 'w') as f:
    f.writelines( lines )




# update README.md
fpath = os.path.join(dirREPO, 'README.md')
with open(fpath, 'r') as f:
    lines = f.readlines()
    for i,line in enumerate(lines):
        if line.startswith('![version]'):
            break
    lines[i] = f"![version](https://img.shields.io/badge/version-{version_str}-blue)\n"
with open(fpath, 'w') as f:
    f.writelines( lines )

