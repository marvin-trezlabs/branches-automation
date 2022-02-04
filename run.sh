#!/usr/bin/env bash

# Using the set -a option where "Each variable or function that is created
#  or modified is given the export attribute and marked for export to the environment of subsequent commands".
set -a
source config.env
set +a

python3 script.py --date=2022-02-05 --deleteall=true --dryrun=true