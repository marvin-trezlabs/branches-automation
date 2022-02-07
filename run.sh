#!/usr/bin/env bash

# Using the set -a option where "Each variable or function that is created
#  or modified is given the export attribute and marked for export to the environment of subsequent commands".
set -a
source config.env
set +a

# Testing (default base branch: Main )
python3 script.py --date=2022-02-08 --base-branch=main

#If you want to delete, pass the --delete-all flag like the example:
# python3 script.py --date=2022-02-08 --delete-all

# If you want to specify a different base branch name, pass the --base-branch flag as follows:
# python3 script.py --date=2022-02-08 --base-branch=master --delete-all

# Protect branches that you dont want to be deleted even if appears in the Plan / report phase. Default: main
# python3 script.py --date=2022-02-08 --base-branch=main --protect my_protected_merged_branch main
