#!/usr/bin/env bash

# Using the set -a option where "Each variable or function that is created
#  or modified is given the export attribute and marked for export to the environment of subsequent commands".
set -a
source config.env
set +a

# Testing (default base branch: Main )
python3 script.py --date=2022-02-08 --base-branch=my_branch --delete-all

#If you want to delete, pass the --delete-all flag like the example:
# python3 script.py --date=2022-02-08 --delete-all

# If you want to specify a different base branch name, pass the --base-branch flag as follows:
# python3 script.py --date=2022-02-08 --base-branch=master --delete-all