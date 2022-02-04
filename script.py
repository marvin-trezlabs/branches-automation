#!/usr/bin/env python3
import json
import os
import pprint
import requests
import argparse
from datetime import datetime

parser = argparse.ArgumentParser()

parser.add_argument("--dry-run", help="Run in report mode or dry run")
parser.add_argument("--date", action="store_true", default="2022-01-16", 
    help="Date umbral in format 2022-01-28. This will include that date and olders to fetch the report.")

args = parser.parse_args()

token = os.getenv('GITHUB_TOKEN', '...')
owner = "razchen"
repo = "roberto_oceano"

date = args.date + 'T0:0:0Z'
# print(date)

umbralDate = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S%z")

url = "https://api.github.com/repos/" + owner +"/"+ repo + "/branches"
# print(url)
headers = {'Authorization': f'token {token}'}

response = requests.get(url, headers=headers)
branches = response.json()
# print(branches)
# print(args.date)
# print(umbralDate)

        
for branches in branches:
    print('BRANCHES: ' + branches['name'])
    branchName = branches['name']
    response2 = requests.get(branches['commit']['url'], headers=headers)
    jsondata = response2.json()

    branchDate = jsondata['commit']['author']['date']
    branchDate = datetime.strptime(branchDate, "%Y-%m-%dT%H:%M:%S%z")
    # pprint.pprint("Latest commit Date:" + branchDate)
    # print(branchDate <= umbralDate)
     
    if(branchDate <= umbralDate) :    
        url = "https://api.github.com/repos/" + owner + "/" + repo + "/pulls?state=all&head="+ owner + ":" + branchName

        response3 = requests.get(url, headers=headers)
        pprint.pprint(response3.json())
  
    # https://github.com/CogWorksBWSI/GitPracticeRepo
    # Fork and make testings with that repo

    # Get merged branches into main/paramenter branch (THis is on pull request endpoint, 
    # with branch name as a paramenter and check merged_at attribute)

    #Delete that branch if parameter was provided

    #VALIDATE if a branch is present in various pull request and was already deleted from the script.
    
    #If dry-run, just present a report to a file or stdout

# pprint.pprint(response.json())

