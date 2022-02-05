#!/usr/bin/env python3
import os
import requests
import argparse
from datetime import datetime

parser = argparse.ArgumentParser()

# Defining arguments
parser.add_argument("--dryrun", help="Set this flag to True to run in safe/report mode", default=False, type=bool)
parser.add_argument("--date", help="Date umbral in format 2022-01-28. This will include that date and olders to fetch the report.", type=str)
parser.add_argument("--deleteall", help="Set this flag to True if wants to delete all", default=False, type=bool)

args = parser.parse_args()

# Getting Token from ENV
token = os.getenv('GITHUB_TOKEN', '...')
# Variables (Maybe convert to ENV)
owner = "marvin-trezlabs"
repo = "GitPracticeRepo"

# Formating date
date = args.date + 'T0:0:0Z'
umbralDate = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S%z")

# Getting criteria from params
userWantsToDelete = True if args.deleteall == True else False
isDryRun = True if args.dryrun == True else False

# Setting authorization headers
headers = {'Authorization': f'token {token}'}

# Fetching branches
url = "https://api.github.com/repos/" + owner +"/"+ repo + "/branches"
response = requests.get(url, headers=headers)
branches = response.json()

# Printing info
print('Criteria:')
print('  Delete: ' + str(userWantsToDelete))
print('  Is dry run: ' + str(isDryRun))
print('  Date: Older than ' + str(umbralDate))
print('Searching.........\n')

# empty results variable
branchesFound = []

# Looping branches 
for br in branches:
    branchName = br['name']
    # Fetching the head commit in order to get the latest commit date
    response2 = requests.get(br['commit']['url'], headers=headers)
    jsondata = response2.json()

    # Extracting the date 
    branchDate = jsondata['commit']['author']['date']
    branchDate = datetime.strptime(branchDate, "%Y-%m-%dT%H:%M:%S%z")
    
    #  Checking if the date is in the interval
    if(branchDate <= umbralDate) :    
        print('Found BRANCH: ' + br['name'])
        branchesFound.append(br['name'])

        # Fetching the pull requests of that branches to determine if was merged or not
        url = "https://api.github.com/repos/" + owner + "/" + repo + "/pulls?state=all&head="+ owner + ":" + branchName
        response3 = requests.get(url, headers=headers)
        pullRequests = response3.json()
        
        # Looping PR 
        for pullRequest in pullRequests:
            # Extracting if was merged bool 
            wasMerged = bool(pullRequest['merged_at']) if pullRequest['merged_at'] else False

            # Printing info 
            print(' -- Pull Request: ' + pullRequest['title'] )
            print(" -- Merged : " + str(wasMerged))
            if(wasMerged):
                print(" -- Merged at date: " + pullRequest['merged_at'])
                print(" -- Pass the '--deleteall=true' to delete : ")

            # Checking flags to determine if proceed to delete
            if(wasMerged == True and userWantsToDelete == True and not isDryRun ) :
                # Deleting the branch
                urlDelete = "https://api.github.com/repos/"+ owner + "/" + repo + "/git/refs/heads/" + branchName
                responseDelete = requests.delete(urlDelete, headers=headers)
                print('deleting merged branch...')
                if(responseDelete.status_code) :
                    print('✔ Deleted successfully')
                else :
                    print('✖ Failed to delete')
                break

# Empty results
if(len(branchesFound) <=0 ):
    print('NOT found branches that match the Criteria')


